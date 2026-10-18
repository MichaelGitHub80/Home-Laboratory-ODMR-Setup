# Copyright (c) 2026 Michael Herrmann
# This software is released under the MIT License.
# See the LICENSE file in the project root for more information.

import time
import os
import socket
import csv
from datetime import datetime
import numpy as np
import cv2
import matplotlib.pyplot as plt
import zwoasi as asi

from scipy.signal import savgol_filter

USE_RASPBERRY = True

# --- 1. ZWO SDK DLL Pfad initialisieren ---
DLL_DIR = r"\ZWO ASI 585 MC color"
dll_path = os.path.join(DLL_DIR, "ASICamera2.dll")

if not os.path.exists(dll_path):
    raise FileNotFoundError(f"Die SDK-DLL wurde unter {dll_path} nicht gefunden!")

os.environ['ZWO_ASI_LIB'] = dll_path
asi.init(dll_path)
print("--> ZWO SDK erfolgreich initialisiert!")

# --- 2. Kamera initialisieren ---
num_cams = asi.get_num_cameras()
if num_cams <= 0:
    print("FEHLER: Keine Kamera gefunden!")
    exit()

camera = asi.Camera(0)
camera.stop_video_capture()
camera.stop_exposure()
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, 40)

# Parameter aus SharpCap
sharpcap_schwenk = 1792
sharpcap_tilt = 1048
roi_w = 320
roi_h = 240       

sharpcap_start_x = (sharpcap_schwenk // 8) * 8
sharpcap_start_y = (sharpcap_tilt // 2) * 2

print(f"Setze fokussierte NV-ROI: {roi_w} x {roi_h} bei X={sharpcap_start_x}, Y={sharpcap_start_y}...")
camera.set_roi(start_x=sharpcap_start_x, start_y=sharpcap_start_y, width=roi_w, height=roi_h, image_type=asi.ASI_IMG_RAW16)

# --- 4. Kamera-Steuerwerte ---
camera.set_control_value(asi.ASI_EXPOSURE, 60000)     # 60 ms Belichtung
camera.set_control_value(asi.ASI_GAIN, 252)            
camera.set_control_value(asi.ASI_WB_B, 100)
camera.set_control_value(14, 0)                        
camera.set_control_value(13, 0)                        
camera.set_control_value(5, 0)        

# --- 5. SWEEP-PARAMETER (2-MHz-Schritte von 2.75 bis 3.00 GHz) ---
NUM_FRAMES_PER_STEP = 3
ADF_LOCK_TIME = 0.05

# 2-MHz-Schritte ergeben 126 Punkte
start_freq = 2.700
end_freq = 3.000
freq_width = 0.001
steps = int((end_freq - start_freq) / freq_width)
freqs = [round(start_freq + i * freq_width, 3) for i in range(steps)]

TOTAL_STEPS = len(freqs)
odmr_raw_records = [] 
odmr_data = []

# --- 6. Netzwerkverbindung ---
s = None
if USE_RASPBERRY:
    print("Verbinde mit Raspberry Pi (192.168.0.161:5005)...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.161", 5005))

# --- 7. Plot Setup ---
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'ro-', label="Normierte Intensität (I_sig / I_ref)") 
trend_line, = ax.plot([], [], 'g-', linewidth=2, label="Savitzky-Golay Trend") 
ax.grid(True)
ax.set_xlabel("Frequenz (GHz)")
ax.set_ylabel("Normiertes Signal (16-Bit Ratio)")
ax.set_title("PRÄZISIONS-ODMR-SWEEP (RAW16 Differenzmessung)")
ax.legend(loc="upper right")

camera.start_video_capture()
time.sleep(0.5)

# --- LIVE-VORSCHAU ---
print("\nÖFFNE LIVE-VORSCHAU (SPACE DRÜCKEN FÜR SWEEP)...")
while True:
    try:
        img_preview = camera.capture_video_frame(timeout=2000)
        if img_preview is not None:
            img_min, img_max = np.min(img_preview), np.max(img_preview)
            img_8bit = ((img_preview - img_min) / (img_max - img_min) * 255).astype(np.uint8) if img_max > img_min else np.zeros_like(img_preview, dtype=np.uint8)
            img_color = cv2.cvtColor(img_8bit, cv2.COLOR_GRAY2BGR)
            img_color[:, :, 0] = 0  
            img_color[:, :, 1] = 0  
            cv2.putText(img_color, "Drücke [SPACE] für Sweep-Start", (10, roi_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.imshow("NV-Diamant ROI Vorschau (Belichtung/Justage)", img_color)
        if cv2.waitKey(1) & 0xFF == 32:  
            cv2.destroyWindow("NV-Diamant ROI Vorschau (Belichtung/Justage)")
            break
    except asi.ZWO_IOError:
        break

# --- OPTIMIERTE MESSFUNKTION ---
def capture_averaged_frame(n):
    try:
        camera.flush_video_capture_buffer() 
    except AttributeError:
        for _ in range(2):
            _ = camera.capture_video_frame(timeout=100)
            
    frames = []
    for _ in range(n):
        try:
            img = camera.capture_video_frame(timeout=500)
            if img is not None: 
                frames.append(img)
        except asi.ZWO_IOError: 
            break
            
    if len(frames) == 0: 
        return np.zeros((roi_h, roi_w), dtype=np.uint16)
    return np.mean(frames, axis=0).astype(np.uint16)


def read_line_from_pi(sock):
    buffer = ""
    while "\n" not in buffer:
        data = sock.recv(1).decode()
        if not data: raise ConnectionResetError("Verbindung zum Pi verloren.")
        buffer += data
    return buffer.strip()

print("\nStarte optimierte High-Speed-Messschleife...")

try:
    for idx, f in enumerate(freqs):
        # --- MESSUNG A: SIGNAL ---
        if USE_RASPBERRY:
            f_mhz = int(round(f * 1000))
            s.sendall(f"{f_mhz}\n".encode())
            pi_response = read_line_from_pi(s)
            if "LOCKED" not in pi_response: continue

        time.sleep(ADF_LOCK_TIME)
        avg_signal_frame = capture_averaged_frame(NUM_FRAMES_PER_STEP)
        i_sig = np.mean(avg_signal_frame)

        # --- MESSUNG B: REFERENZ ---
        if USE_RASPBERRY:
            s.sendall("OFF\n".encode())
            pi_response = read_line_from_pi(s)
            if "OFF_DONE" not in pi_response: continue

        time.sleep(ADF_LOCK_TIME)
        avg_ref_frame = capture_averaged_frame(NUM_FRAMES_PER_STEP)
        i_ref = np.mean(avg_ref_frame)

        # --- AUSWERTUNG ---
        norm_ratio = i_sig / i_ref
        
        if np.isnan(norm_ratio) or np.isinf(norm_ratio):
            norm_ratio = 1.0  
        print(f"Schritt {idx:03d}/{TOTAL_STEPS:03d} | Freq: {f:.3f} GHz | Ratio: {norm_ratio:.5f}")
        
        odmr_data.append((f, norm_ratio))
        odmr_raw_records.append([f, i_sig, i_ref, norm_ratio])

        x_shot = [x[0] for x in odmr_data]
        y_shot = [x[1] for x in odmr_data]
        line.set_xdata(x_shot)
        line.set_ydata(y_shot)
        ax.set_xlim(min(freqs) - 0.005, max(freqs) + 0.005)
        
        if len(y_shot) > 1: 
            ax.set_ylim(min(y_shot) - 0.001, max(y_shot) + 0.001)
            
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.001)

        if cv2.waitKey(1) == 27: break

    if len(odmr_raw_records) > 0:
        target_dir = r"\Sweep\run"
        if not os.path.exists(target_dir): 
            os.makedirs(target_dir)
        filename = f"odmr_differential_sweep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_full_path = os.path.join(target_dir, filename)
        
        print(f"\nSpeichere Messdaten in: {csv_full_path} ...")
        with open(csv_full_path, mode='w', newline='') as f_csv:
            writer = csv.writer(f_csv, delimiter=';')
            writer.writerow(["Frequenz_GHz", "I_Signal_Raw16", "I_Referenz_Raw16", "Ratio_Sig_Ref"])
            writer.writerows(odmr_raw_records)
        print("--> CSV erfolgreich gespeichert!")

    if len(odmr_data) > 15:
        print("\nBerechne mathematischen Savitzky-Golay Trend...")
        # Korrigiert: Extraktion aus den Datentupeln
        x_arr = np.array([x[0] for x in odmr_data])
        y_arr = np.array([x[1] for x in odmr_data])
        
        # Fenstergröße 11 Messpunkte, Polynomordnung 3
        y_smooth = savgol_filter(y_arr, window_length=11, polyorder=3)
        
        trend_line.set_xdata(x_arr)
        trend_line.set_ydata(y_smooth)
        ax.legend(loc="upper right")
        fig.canvas.draw()
        fig.canvas.flush_events()
        print("Savitzky-Golay Trend erfolgreich eingezeichnet!")

        plt.ioff()
        plt.show()

except KeyboardInterrupt:
    print("\nMessung abgebrochen.")
finally:
    if len(odmr_raw_records) > 0 and 'csv_full_path' not in locals():
        target_dir = r"C:\Michael\Coding\python\ODMR\Sweep\run"
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        filename = f"odmr_interrupted_sweep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(os.path.join(target_dir, filename), mode='w', newline='') as f_csv:
            writer = csv.writer(f_csv, delimiter=';')
            writer.writerow(["Frequenz_GHz", "I_Signal_Raw16", "I_Referenz_Raw16", "Ratio_Sig_Ref"])
            writer.writerows(odmr_raw_records)
        print(f"--> Notfall-CSV bei Abbruch gespeichert unter: {filename}")
        
    cv2.destroyAllWindows()
    camera.close()
    if s is not None: s.close()
    print("Hardware geschlossen.")