@echo off
title ODMR Pi-Sweep Starter 
echo ====================================================
echo Beende alte Sweep-Skripte auf dem Pi...
echo ====================================================

ssh dell@raspberrypi "pkill -f sweep_raspberry.py" 2>nul
timeout /t 1 /nobreak >nul

echo ====================================================
echo [1/2] Kopiere sweep_raspberry.py zum Pi via SCP...
echo ====================================================
scp "C:\...\sweep_raspberry.py" 
dell@raspberrypi:/home/dell/raspberrypy/ODMR/sweep_raspberry.py

echo.
echo ====================================================
echo [2/2] Starte ODMR Hardware-Sweep via UDP auf dem Pi...
echo ====================================================
ssh dell@raspberrypi "cd /home/dell/raspberrypy/ODMR && python3 sweep_raspberry.py"

pause
