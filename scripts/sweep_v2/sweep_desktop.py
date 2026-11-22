# Copyright (c) 2026 Michael Herrmann
# This software is released under the MIT License.
# See the LICENSE file in the project root for more information.

import os
import time
import socket
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import cv2  

# ZWO SDK Pfad registrieren
os.environ['PATH'] = r"C:\Michael\coding\python\ODMR" + os.pathsep + os.environ.get('PATH', '')
import zwoasi as asi

DLL_DIR = r"C:\Michael\coding\python\ODMR"
dll_path = os.path.join(DLL_DIR, "ASICamera2.dll")
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"Die SDK-DLL wurde unter {dll_path} nicht gefunden!")
os.environ['ZWO_ASI_LIB'] = dll_path
asi.init(dll_path)

# Kamera initialisieren & feste Messparameter einmalig setzen
camera = asi.Camera(0)
camera.stop_video_capture()
camera.stop_exposure()
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, 40)

# Messparameter für Kamera
EXPOSURE_US = 3000        # ms Belichtungszeit
GAIN_VAL = 252            # High Conversion Gain (HCG)
camera.set_control_value(asi.ASI_EXPOSURE, EXPOSURE_US)
camera.set_control_value(asi.ASI_GAIN, GAIN_VAL)            
camera.set_control_value(asi.ASI_WB_B, 100)

# ==========================================================
# NEUE STEUERUNGSPARAMETER (DIREKT VOM DESKTOP AUS)
# ==========================================================
ADF_POWER_LEVEL = 1       # Einstellbar: 0 (-4 dBm), 1 (-1 dBm), 2 (+2 dBm), 3 (+5 dBm)
POWER_DBM_MAP = {0: "-4.0 dBm", 1: "-1.0 dBm", 2: "+2.0 dBm", 3: "+5.0 dBm"}
MASK_PERCENTILE = 90      # Nur die hellsten x % der Pixel im 64x64 ROI auswerten
DARK_OFFSET = 741        # Kamera-Bias bei Gain 252 (in 16-Bit ADU)

# Sweep-Parameter & nahe Referenzfrequenz gegen thermisches Pumpen
start_freq_ghz = 2.765
end_freq_ghz = 2.96
step_size_ghz = 0.005
REF_FREQ_GHZ = 2.7500
N_AVGS = 15

# Exakte Koordinaten aus der Heatmap-Suche
roi_w, roi_h = 64, 64
start_x, start_y = 1214, 1060
                
# ==========================================================
# PHASE 1: VOLLBILD-AUSRICHTUNG MIT RGB LIVE-VORSCHAU
# ==========================================================
print("\n==========================================================")
print(" PHASE 1: Kamera im Vollbild-Modus (RGB Live-Vorschau)")
print(" --> DRÜCKE DIE LEERTASTE (SPACE), UM WEITERZUGEHEN!")
print("==========================================================")

camera.set_roi(start_x=0, start_y=0, width=3840, height=2160, image_type=asi.ASI_IMG_RAW16) 
cv2.namedWindow("ODMR - Sensor-Ausrichtung (RGB Full Chip)", cv2.WINDOW_NORMAL)
cv2.resizeWindow("ODMR - Sensor-Ausrichtung (RGB Full Chip)", 800, 450)

camera.start_video_capture()

saved_preview_img = None

while True:
    try:
        img_full = camera.capture_video_frame(timeout=200)
        if img_full is not None:
            img_disp = cv2.normalize(img_full, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            img_rgb = cv2.cvtColor(img_disp, cv2.COLOR_BayerBG2BGR)
            
            # Saubere Kopie nur mit ROI-Rechteck (ohne den "LEERTASTE DRUECKEN"-Text) für die Speicherung
            img_clean_save = img_rgb.copy()
            cv2.rectangle(img_clean_save, (start_x, start_y), (start_x + roi_w, start_y + roi_h), (0, 0, 255), 3)
            
            cv2.rectangle(img_rgb, (start_x, start_y), (start_x + roi_w, start_y + roi_h), (0, 0, 255), 2)
            cv2.putText(img_rgb, "LEERTASTE DRUECKEN FUER MESS-START", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
            
            cv2.imshow("ODMR - Sensor-Ausrichtung (RGB Full Chip)", img_rgb)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '): 
                saved_preview_img = img_clean_save
                print(f"\n[OK] Nutze Heatmap-Koordinaten ({start_x}, {start_y})!")
                break
            elif key == ord('q'):
                print("Programm abgebrochen.")
                camera.stop_video_capture()
                exit()
    except asi.ZWO_IOError:
        continue


print("\n--> Schließe Phase 1... Stoppe Video-Capture...")
camera.stop_video_capture()
cv2.destroyAllWindows()
time.sleep(0.3) 

# ==========================================================
# PHASE 1.5: EINZELBILD-MESSMODUS (SNAP) & PIXEL-MASKE
# ==========================================================
print(f"\n=== SCHALTE KAMERA IN DEN {roi_w}x{roi_h} SNAP-MESSMODUS ===")
camera.set_roi(start_x=start_x, start_y=start_y, width=roi_w, height=roi_h, image_type=asi.ASI_IMG_RAW16)
time.sleep(0.2)

# Erste 2 Frames nach ROI-Wechsel still verwerfen (Puffer- & Sensor-Stabilisierung)
for _ in range(2):
    _ = camera.capture()

# Netzwerkverbindung zum Pi via Ethernet
PI_IP = "192.168.0.161"
PI_PORT = 5005
net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
net.connect((PI_IP, PI_PORT))
net.settimeout(5.0) 

# Power Level an Raspberry Pi senden
print(f"--> Sende ADF4351 Power Level {ADF_POWER_LEVEL} an Raspberry Pi...")
net.sendall(f"POWER:{ADF_POWER_LEVEL}\n".encode())
try:
    resp_pwr = net.recv(1024).decode().strip()
    print(f"[PI-ANTWORT] {resp_pwr}")
except socket.timeout:
    print("[INFO] Keine direkte Quittung für POWER-Befehl.")

# Mikrowelle für Referenzbild-Aufnahme sicher ausschalten
net.sendall(b"OFF\n")
_ = net.recv(1024)
time.sleep(0.1)

print(f"--> Berechne statische Pixel-Maske (>{MASK_PERCENTILE}. Perzentil im {roi_w}x{roi_h} ROI)...")
ref_stack = []
for _ in range(15):
    frame = camera.capture()
    if frame is not None:
        ref_stack.append(frame.astype(np.float64))

mean_ref_img = np.mean(ref_stack, axis=0) - DARK_OFFSET
threshold_val = np.percentile(mean_ref_img, MASK_PERCENTILE)
PIXEL_MASK = mean_ref_img > threshold_val
active_pixels = int(np.sum(PIXEL_MASK))
print(f"[OK] Pixel-Maske aktiv: {active_pixels} von {roi_w*roi_h} Pixeln ausgewählt (Schwelle: {threshold_val:.1f} ADU).")

# ==========================================================
# PHASE 2: AUSWERTUNG & THERMISCH STABILER SWEEP
# ==========================================================
def extract_masked_signal(raw16_img):
    if raw16_img is None:
        return 0.0
    img_corr = raw16_img.astype(np.float64) - DARK_OFFSET
    return float(np.mean(img_corr[PIXEL_MASK]))

freqs = [round(start_freq_ghz + i * step_size_ghz, 4) for i in range(int((end_freq_ghz - start_freq_ghz) / step_size_ghz) + 1)]

# Live plot setup
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8.8))

pwr_str = f"Level {ADF_POWER_LEVEL} ({POWER_DBM_MAP.get(ADF_POWER_LEVEL, '?')})"
exp_ms = EXPOSURE_US / 1000.0
step_mhz = step_size_ghz * 1000.0

info_header = (
    f"CW-ODMR Measurement Protocol (Snap-Sync)  |  MW: ADF4351 {pwr_str}  |  ROI: {roi_w}x{roi_h} @ ({start_x}, {start_y})\n"
    f"Camera: Exp {exp_ms:.1f} ms, Gain {GAIN_VAL}  |  Mask: >{MASK_PERCENTILE}% ({active_pixels} px, Dark {DARK_OFFSET:.0f})  |  "
    f"Sweep: {start_freq_ghz:.3f}–{end_freq_ghz:.3f} GHz (Step {step_mhz:.1f} MHz, Avg {N_AVGS}x)"
)
fig.suptitle(info_header, fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0f4f8', edgecolor='#b0c4de'))

line_off,  = ax1.plot([], [], color='green', marker='x', linestyle='--', markersize=3, label='Reference (MW OFF)')
line_on,   = ax1.plot([], [], color='red', marker='o', linestyle='-', markersize=3, label=f'Signal (MW ON, {pwr_str})')
line_norm, = ax2.plot([], [], color='blue', marker='o', linestyle='-', markersize=4, label=f'Normalized Contrast (Mask >{MASK_PERCENTILE}%)')

ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_title("Raw PL Intensity (Signal vs. Reference)", fontsize=10.5, fontweight='bold')
ax1.set_ylabel("Intensity (Counts - Dark)", fontsize=9)
ax1.legend(loc="upper left")
ax1.set_xlim(start_freq_ghz, end_freq_ghz)

ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_title("Normalized Quantum Spectrum ($I_{\\text{Signal}} / I_{\\text{Reference}}$)", fontsize=10.5, fontweight='bold')
ax2.set_xlabel("Microwave Frequency (GHz)", fontsize=9)
ax2.set_ylabel("Normalized PL Intensity (a.u.)", fontsize=9)
ax2.axhline(1.0000, color='black', linestyle=':', alpha=0.6)
ax2.set_xlim(start_freq_ghz, end_freq_ghz)
ax2.legend(loc="upper right")
plt.tight_layout(rect=[0, 0, 1, 0.92])


print(f"\n--> Wärme Verstärker & Stripline 3 Sekunden auf {REF_FREQ_GHZ} GHz vor...")
net.sendall(f"{REF_FREQ_GHZ:.4f}\n".encode())
_ = net.recv(1024)
time.sleep(3.0)

valid_freqs = []
raw_on_intensities = []
raw_off_intensities = []
intensities = []

print("==========================================================")
print(" THERMISCH STABILER SNAP-SWEEP GESTARTET...")
print("==========================================================")

try:
    for idx, f in enumerate(freqs):
        ion_list = []
        ioff_list = []
        ratio_list = []

        for _ in range(N_AVGS):
            val_on = 0.0
            val_off = 0.0

            try:
                # 1. SIGNAL (MW ON)
                net.sendall(f"{f:.4f}\n".encode())
                resp = net.recv(1024).decode().strip()
                if "LOCKED" in resp:
                    time.sleep(0.002)
                    val_on = extract_masked_signal(camera.capture())

                # 2. REFERENZ (HMC284 -> DUMMY LOAD)
                net.sendall(b"OFF\n")
                resp_off = net.recv(1024).decode().strip()
                if "OFF_DONE" in resp_off:
                    time.sleep(0.002)
                    val_off = extract_masked_signal(camera.capture())
            except socket.timeout:
                print(f"[WARNUNG] Timeout bei {f:.4f} GHz – überspringe Einzelmessung...")
                continue


            # Paarweise Normalisierung gegen Drift
            if val_on > 0 and val_off > 0:
                ion_list.append(val_on)
                ioff_list.append(val_off)
                ratio_list.append(val_on / val_off)

        # --- AUSWERTUNG & PLOT-UPDATE ---
        if len(ratio_list) > 0:
            i_on = float(np.mean(ion_list))
            i_off = float(np.mean(ioff_list))
            contrast = float(np.mean(ratio_list))

            valid_freqs.append(f)
            intensities.append(contrast)
            raw_on_intensities.append(i_on)
            raw_off_intensities.append(i_off)

            print(f"[ODMR] [{idx+1}/{len(freqs)}] Freq: {f:.4f} GHz | I_on: {i_on:.1f} | I_off: {i_off:.1f} | Kontrast: {contrast:.4f}")

            x_data = np.array(valid_freqs)
            y_data = np.array(intensities)

            line_on.set_data(x_data, np.array(raw_on_intensities))
            line_off.set_data(x_data, np.array(raw_off_intensities))

            all_raw = raw_on_intensities + raw_off_intensities
            ax1.set_ylim(min(all_raw) - 50, max(all_raw) + 50)



            line_norm.set_data(x_data, y_data)
            if len(y_data) > 1:
                ax2.set_ylim(min(y_data) - 0.0015, max(y_data) + 0.0015)

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.001)

except KeyboardInterrupt:
    print("\nMessung manuell abgebrochen.")
finally:
    print("--> Schalte Mikrowelle am Raspberry Pi komplett ab (OFF)...")
    try:
        net.sendall(b"OFF\n")
    except Exception:
        pass
    try:
        camera.stop_video_capture()
    except Exception:
        pass
    net.close()
    plt.ioff()


# ==========================================================
# CSV-EXPORT, SAVITZKY-GOLAY TREND & PNG-SPEICHERUNG
# ==========================================================
if len(valid_freqs) > 0:
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    target_dir = r"C:\Michael\coding\python\ODMR\Sweep"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    base_filename = f"odmr_roi{start_x}_{start_y}_exp{int(exp_ms)}ms_avg{N_AVGS}_mask{MASK_PERCENTILE}_pwr{ADF_POWER_LEVEL}_{timestamp_str}"
    csv_path = os.path.join(target_dir, base_filename + ".csv")
    with open(csv_path, mode='w', newline='') as f_csv:
        writer = csv.writer(f_csv, delimiter=';')
        writer.writerow(["Frequenz_GHz", "I_on", "I_ref", "Kontrast"])
        for f, ion, ioff, c in zip(valid_freqs, raw_on_intensities, raw_off_intensities, intensities):
            writer.writerow([f, ion, ioff, c])
    print(f"\n--> CSV GESPEICHERT UNTER: {csv_path}")

    if len(valid_freqs) > 10:
        from scipy.optimize import curve_fit

        x_fit = np.array(valid_freqs)
        y_fit = np.array(intensities)

        # Double Lorentzian function for split Zero-Field / Zeeman ODMR dips
        def double_lorentzian_dip(f, y0, A1, f1, gamma1, A2, f2, gamma2):
            dip1 = A1 * (0.5 * gamma1)**2 / ((f - f1)**2 + (0.5 * gamma1)**2)
            dip2 = A2 * (0.5 * gamma2)**2 / ((f - f2)**2 + (0.5 * gamma2)**2)
            return y0 - dip1 - dip2

        try:
            y0_init = float(np.median(y_fit))
            amp_init = max(0.0015, (y0_init - float(np.min(y_fit))) * 0.85)
            center_init = float(x_fit[np.argmin(y_fit)])

            # Initial guess: two dips split by ~12 MHz around center
            p0 = [
                y0_init,
                amp_init, center_init - 0.006, 0.018,
                amp_init, center_init + 0.006, 0.018
            ]

            bounds_low  = [0.95, 0.0,  2.830, 0.003, 0.0,  2.840, 0.003]
            bounds_high = [1.05, 0.20, 2.900, 0.100, 0.20, 2.910, 0.100]

            popt, pcov = curve_fit(
                double_lorentzian_dip, x_fit, y_fit,
                p0=p0,
                bounds=(bounds_low, bounds_high),
                maxfev=10000
            )
            perr = np.sqrt(np.diag(pcov))

            y0_opt, A1_opt, f1_opt, g1_opt, A2_opt, f2_opt, g2_opt = popt

            # Ensure f1 is always the lower frequency dip and f2 the higher one
            if f1_opt > f2_opt:
                f1_opt, f2_opt = f2_opt, f1_opt
                A1_opt, A2_opt = A2_opt, A1_opt
                g1_opt, g2_opt = g2_opt, g1_opt
                perr = [perr[0], perr[4], perr[5], perr[6], perr[1], perr[2], perr[3]]

            D_center = 0.5 * (f1_opt + f2_opt)
            E_split_mhz = 0.5 * abs(f2_opt - f1_opt) * 1000.0
            c1_pct, c2_pct = A1_opt * 100.0, A2_opt * 100.0
            fwhm1_mhz, fwhm2_mhz = g1_opt * 1000.0, g2_opt * 1000.0

            x_dense = np.linspace(min(x_fit), max(x_fit), 500)
            y_dense = double_lorentzian_dip(x_dense, *popt)

            # Plot total double fit and individual sub-dips
            total_fit_contrast_pct = (y0_opt - np.min(y_dense)) * 100.0
            raw_peak_contrast_pct  = (y0_opt - np.min(y_fit)) * 100.0

            # Plot total double fit and individual sub-dips
            ax2.plot(
                x_dense, y_dense, color='red', linestyle='-', linewidth=2.2,
                label=(
                    f'Double Lorentzian: D={D_center:.4f} GHz | E={E_split_mhz:.1f} MHz | '
                    f'Contrast: {total_fit_contrast_pct:.2f}% (Peak: {raw_peak_contrast_pct:.2f}%)\n'
                    f'Dip1: {f1_opt:.4f} GHz ({c1_pct:.2f}%, {fwhm1_mhz:.1f} MHz) | '
                    f'Dip2: {f2_opt:.4f} GHz ({c2_pct:.2f}%, {fwhm2_mhz:.1f} MHz)'
                )
            )
            ax2.plot(x_dense, y0_opt - A1_opt * (0.5 * g1_opt)**2 / ((x_dense - f1_opt)**2 + (0.5 * g1_opt)**2),
                     color='orange', linestyle='--', linewidth=1.1, alpha=0.8)
            ax2.plot(x_dense, y0_opt - A2_opt * (0.5 * g2_opt)**2 / ((x_dense - f2_opt)**2 + (0.5 * g2_opt)**2),
                     color='purple', linestyle='--', linewidth=1.1, alpha=0.8)

            ax2.axvline(D_center, color='red', linestyle='--', alpha=0.7)
            ax2.axvline(2.870, color='darkblue', linestyle=':', linewidth=1.5, label='Zero-Field Ref (2.8700 GHz)')
            ax2.legend(loc="lower right", fontsize=8.0)
            fig.canvas.draw()


            print("\n==========================================================")
            print(" DOUBLE LORENTZIAN FIT RESULTS:")
            print(f" -> Center Frequency D     : {D_center:.5f} GHz")
            print(f" -> Splitting Parameter E  : {E_split_mhz:.2f} MHz")
            print(f" -> Dip 1 (f1)             : {f1_opt:.5f} ± {perr[2]:.5f} GHz | Contrast: {c1_pct:.3f}% | FWHM: {fwhm1_mhz:.1f} MHz")
            print(f" -> Dip 2 (f2)             : {f2_opt:.5f} ± {perr[5]:.5f} GHz | Contrast: {c2_pct:.3f}% | FWHM: {fwhm2_mhz:.1f} MHz")
            print(f" -> Baseline y0            : {y0_opt:.5f}")
            print("==========================================================")

        except Exception as e:
            print(f"\n[FIT ERROR] Double Lorentzian fit failed: {e}")


    png_path = os.path.join(target_dir, base_filename + ".png")
    fig.savefig(png_path, dpi=200, bbox_inches='tight')
    print(f"--> PLOT-BILD GESPEICHERT UNTER: {png_path}")
    
    # ZWO ASI Kamerabild mit ROI-Markierung und Key-Daten speichern
    if saved_preview_img is not None:
        cam_img_copy = saved_preview_img.copy()
        overlay_text_1 = f"ZWO ASI585MC | ROI: {roi_w}x{roi_h} @ ({start_x}, {start_y}) | Exp: {exp_ms:.1f} ms | Gain: {GAIN_VAL}"
        overlay_text_2 = f"MW: ADF4351 {pwr_str} | Mask: >{MASK_PERCENTILE}% ({active_pixels} px) | {timestamp_str}"
        
        cv2.putText(cam_img_copy, overlay_text_1, (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 255), 2)
        cv2.putText(cam_img_copy, overlay_text_2, (40, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 255), 2)
        
        cam_png_path = os.path.join(target_dir, base_filename + "_sensor.png")
        cv2.imwrite(cam_png_path, cam_img_copy)
        print(f"--> SENSOR-BILD GESPEICHERT UNTER: {cam_png_path}")


print("--> Das Plot-Fenster bleibt zur Auswertung geöffnet.")
plt.show()