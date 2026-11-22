# Copyright (c) 2026 Michael Herrmann
# This software is released under the MIT License.
# See the LICENSE file in the project root for more information.

import socket
import time
import spidev
import RPi.GPIO as GPIO

from adf435x import calculate_regs, make_regs, FeedbackSelect

# ==============================================================================
# LEISTUNGS-EINSTELLUNG FÜR DEN ADF4351
# 0 = -4 dBm | 1 = -1 dBm | 2 = +2 dBm | 3 = +5 dBm
# ==============================================================================
CURRENT_POWER_LEVEL = 1  # -1 dBm am Ausgang des ADF4351
# ==============================================================================

# --- 1. GPIO Setup ---
GPIO.setmode(GPIO.BCM)
CE_PIN = 17
LOCK_PIN = 24  

GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.setup(LOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- 2. SPI Setup ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0b00

# --- 3. SPI-Schreibfunktion ---
def write_reg(val):
    spi.xfer2([
        (val >> 24) & 0xFF,
        (val >> 16) & 0xFF,
        (val >> 8) & 0xFF,
        val & 0xFF
    ])
    time.sleep(0.002)

def set_frequency(freq_hz, power_level=3, rf_enable=True):  
    freq_mhz = (float(freq_hz) + 0.1) / 1e6
    ref_freq_mhz = 25.0
    
    INT, MOD, FRAC, output_divider, band_select_div = calculate_regs(
        freq=freq_mhz,
        ref_freq=ref_freq_mhz,
        feedback_select=FeedbackSelect.Fundamental,
        enable_gcd=False  
    )
    
    if FRAC < 0: FRAC = 0
    if FRAC >= 4095: FRAC = 4094
    if MOD >= 4095: MOD = 4094
    
    power_mapping = {0: -4.0, 1: -1.0, 2: 2.0, 3: 5.0}
    dbm_power = power_mapping.get(power_level, 5.0)
    
    registers = make_regs(
        INT=INT, FRAC=FRAC, MOD=MOD,
        output_divider=output_divider,
        band_select_clock_divider=band_select_div,
        output_enable=rf_enable,
        output_power=dbm_power,
        aux_output_enable=False,
        counter_reset=False,
        ld_pin_mode=1  
    )

    for i in range(5, -1, -1):
        write_reg(registers[i])
        time.sleep(0.001)


# --- 4. Hardware initialisieren ---
GPIO.output(CE_PIN, GPIO.HIGH)
time.sleep(0.01)

power_dbm_str = {0: "-4 dBm", 1: "-1 dBm", 2: "+2 dBm", 3: "+5 dBm"}

# --- 5. Socket Server ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 5005))
s.listen(1)

print(f"Mikrowellen-Server aktiv (Eingestellte Leistung: {power_dbm_str[CURRENT_POWER_LEVEL]}). Warte on Laptop...")

try:
    while True:
        conn, addr = s.accept()
        print(f"Verbindung hergestellt: {addr}")
        
        # Hilfsvariable, um die jeweils letzte Frequenz für die OFF-Phase zu speichern
        last_freq_hz = 2870000000  # Standard-Startwert (2.870 GHz)

        try:
            while True:
                raw_data = conn.recv(1024).decode().strip()
                if not raw_data:
                    break
                
                parts = raw_data.split()
                if len(parts) == 0:
                    continue
                
                for part in parts:
                    cmd = part.upper()
                    
                    if cmd == "OFF":
                        print(f"ADF4351 -> Schalte HF-Ausgang aus bei {last_freq_hz / 1e6:.3f} MHz (RF OUT = OFF)")
                        
                        set_frequency(last_freq_hz, power_level=CURRENT_POWER_LEVEL, rf_enable=False)
                        
                        conn.sendall("OFF_DONE\n".encode())
                        
                    else:
                        try:
                            freq_mhz = int(part.strip())
                            freq_hz = int(freq_mhz * 1000000)
                            
                            last_freq_hz = freq_hz
                            
                            print(f"ADF4351 -> Sende an Hardware: {freq_hz} Hz ({freq_mhz} MHz)")
                            set_frequency(freq_hz, power_level=CURRENT_POWER_LEVEL, rf_enable=True)
                            
                            is_locked = False
                            for attempt in range(100): 
                                time.sleep(0.002) 
                                if GPIO.input(LOCK_PIN) == GPIO.HIGH:
                                    is_locked = True
                                    break
                            
                            if is_locked:
                                conn.sendall("LOCKED\n".encode())
                            else:
                                print(f"WARNUNG: Frequenz {freq_mhz} MHz rastet nicht ein!")
                                conn.sendall("UNLOCKED\n".encode())
                                
                        except Exception as e:
                            print(f"HARDWARE-FEHLER bei {part} MHz: {type(e).__name__} - {str(e)}")
                            conn.sendall("ERROR\n".encode())
                            
        except ConnectionResetError:
            print("Verbindung vom Laptop abrupt getrennt.")
        finally:
            conn.close()
            print("Verbindung geschlossen. Warte auf neuen Versuch...")

except KeyboardInterrupt:
    print("\nServer wird heruntegerfahren...")
finally:
    GPIO.cleanup()
    spi.close()
    s.close()