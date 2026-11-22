@echo off
title ODMR Pico Deployer via Raspberry Pi
echo ==========================================================
echo  PICO AUTOMATION: SCP - SSH UPLOAD - RESET
echo ==========================================================
echo.

echo [1/3] Kopiere main.py vom PC zum Raspberry Pi via SCP...
scp "C:\...\main.py" dell@raspberrypi:~/raspberrypy/ODMR/main.py

echo.
echo [2/3] Kopiere Datei vom Pi auf den Pico via mpremote...
ssh dell@raspberrypi "python3 -m mpremote cp /home/dell/raspberrypy/ODMR/main.py :main.py"

echo.
echo [3/3] Fuehre harten Reset auf dem Pico aus...
:: Führt den Befehl aus, ignoriert aber den Verbindungsabbruch beim Reboot
ssh dell@raspberrypi "python3 -m mpremote exec \"import machine; machine.reset()\"" 2>nul

echo.
echo ==========================================================
echo [OK] Prozess beendet. Überprüfe die Ausgaben oben!
echo ==========================================================
echo.
pause
