# Copyright (c) 2026 Michael Herrmann
# This software is released under the MIT License.
# See the LICENSE file in the project root for more information.

import machine
import time

machine.freq(125000000)

# --- PIN DEFINITIONEN ---
PIN_TRIG_IN = 22  # Verbunden mit Pin 22 des Raspberry Pi 3
PIN_HMC_A   = 14  # Ausgang A zum HF-Schalter-IC
PIN_HMC_B   = 15  # Ausgang B zum HF-Schalter-IC

# --- INITIALISIERUNG ---
# Eingang vom Raspberry Pi (mit Pull-Down Widerstand zur Stabilisierung)
trig_in = machine.Pin(PIN_TRIG_IN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Startzustand des Schalters: MW OFF (A=0, B=1 -> Dummy Load)
hmc_a = machine.Pin(PIN_HMC_A, machine.Pin.OUT, value=0)
hmc_b = machine.Pin(PIN_HMC_B, machine.Pin.OUT, value=1)

print("==========================================================")
print(" PICO HARDWARE-TRIGGER BEREIT.")
print(" Lausche auf Flankenwechsel an Pin 22...")
print("==========================================================")

# Extrem schnelle und unzerstörbare Hardware-Schleife
while True:
    if trig_in.value() == 1:
        # Phase A: Pi signalisiert MW_ON -> Schalter umlegen
        hmc_a.value(1)
        hmc_b.value(0)
    else:
        # Phase B: Pi signalisiert MW_OFF -> Dummy Load
        hmc_a.value(0)
        hmc_b.value(1)