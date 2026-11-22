# Copyright (c) 2026 Michael Herrmann
# This software is released under the MIT License.
# See the LICENSE file in the project root for more information.

import socket
import time
import spidev
import RPi.GPIO as GPIO
from adf435x import calculate_regs, make_regs, FeedbackSelect

CURRENT_POWER_LEVEL = 1
LAST_FREQ_GHZ = None
LAST_POWER_LEVEL = None

CE_PIN = 17
PICO_TRIG_PIN = 22
LOCK_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CE_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PICO_TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0b00

def write_reg(val):
    spi.xfer2([(val >> 24) & 0xFF, (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF])
    time.sleep(0.0001)

def set_adf_output(freq_hz, power_level=0):
    freq_mhz = round(float(freq_hz) / 1e6, 4)
    INT, MOD, FRAC, output_divider, band_select_div = calculate_regs(
        freq=freq_mhz, ref_freq=25.0, feedback_select=FeedbackSelect.Fundamental
    )
    power_mapping = {0: -4.0, 1: -1.0, 2: 2.0, 3: 5.0}
    registers = make_regs(
        INT=INT, FRAC=FRAC, MOD=MOD, output_divider=output_divider,
        band_select_clock_divider=band_select_div,
        output_disable=False,
        output_power=power_mapping.get(power_level, -4.0),
        aux_output_enable=False, counter_reset=False, ld_pin_mode=1
    )
    for i in range(5, -1, -1):
        write_reg(registers[i])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 5005))
s.listen(1)

print(f"TCP-Server bereit (Start Power Level {CURRENT_POWER_LEVEL}). Warte auf Desktop-PC...")

while True:
    conn, addr = s.accept()
    print(f"Verbunden mit {addr}")
    LAST_FREQ_GHZ = None
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            for cmd in data.splitlines():
                cmd = cmd.strip()
                if cmd == "OFF":
                    GPIO.output(PICO_TRIG_PIN, GPIO.LOW)
                    conn.sendall(b"OFF_DONE\n")
                elif cmd.startswith("POWER:"):
                    try:
                        new_lvl = int(cmd.split(":")[1])
                        if new_lvl in (0, 1, 2, 3):
                            CURRENT_POWER_LEVEL = new_lvl
                            LAST_POWER_LEVEL = None
                            print(f"[INFO] Power Level gesetzt auf {CURRENT_POWER_LEVEL}")
                            conn.sendall(f"POWER_SET_{CURRENT_POWER_LEVEL}\n".encode())
                        else:
                            conn.sendall(b"POWER_ERR_RANGE\n")
                    except ValueError:
                        conn.sendall(b"POWER_ERR_FORMAT\n")
                        
                elif cmd.startswith("MODE:"):
                    mode_idx = int(cmd.split(":")[1])
                    GPIO.output(PICO_TRIG_PIN, GPIO.LOW)
                    time.sleep(0.32)  # 320 ms Pause -> Pico setzt current_mode_idx sicher auf 0

                    # 2. Exakt 'mode_idx' saubere 1.5-ms-Zählpulse lokal am Pi erzeugen (null Netzwerk-Jitter!)
                    for _ in range(mode_idx):
                        GPIO.output(PICO_TRIG_PIN, GPIO.HIGH)
                        time.sleep(0.0015)   # 1.5 ms HIGH (sicher < 15 ms auf Pico)
                        GPIO.output(PICO_TRIG_PIN, GPIO.LOW)
                        time.sleep(0.0015)   # 1.5 ms LOW

                    conn.sendall(b"MODE_OK\n")
            
 
                else:
                    freq_ghz = float(cmd)
                    # Nur neu programmieren, wenn Frequenz oder Power sich geändert hat
                    if freq_ghz != LAST_FREQ_GHZ or CURRENT_POWER_LEVEL != LAST_POWER_LEVEL:
                        set_adf_output(int(round(freq_ghz * 1e9)), CURRENT_POWER_LEVEL)
                        locked = False
                        for _ in range(100):
                            time.sleep(0.0005)
                            if GPIO.input(LOCK_PIN) == GPIO.HIGH:
                                locked = True
                                break
                        if not locked:
                            conn.sendall(b"UNLOCKED\n")
                            continue
                        LAST_FREQ_GHZ = freq_ghz
                        LAST_POWER_LEVEL = CURRENT_POWER_LEVEL

                    GPIO.output(PICO_TRIG_PIN, GPIO.HIGH)
                    conn.sendall(b"LOCKED\n")
    except Exception as e:
        print(f"Verbindungsfehler: {e}")

    finally:
        GPIO.output(PICO_TRIG_PIN, GPIO.LOW)
        LAST_FREQ_GHZ = None
        conn.close()