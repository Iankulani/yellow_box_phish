@echo off
title YellowBoxPhish Installer v2.0.0
color 0E

echo ╔══════════════════════════════════════════════════════════════╗
echo ║          🐠 YELLOW_BOX_PHISH v2.0.0 - INSTALLATION        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [*] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python 3 not found
    echo [*] Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✔] Python %PYTHON_VERSION% found

echo.
echo [*] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [*] Creating directories...
mkdir .yellow_box_phish 2>nul
mkdir reports 2>nul
mkdir logs 2>nul
mkdir config 2>nul
mkdir data 2>nul
mkdir .yellow_box_phish\payloads 2>nul
mkdir .yellow_box_phish\workspaces 2>nul
mkdir .yellow_box_phish\scans 2>nul
mkdir .yellow_box_phish\nikto_results 2>nul
mkdir .yellow_box_phish\whatsapp_session 2>nul
mkdir .yellow_box_phish\phishing_pages 2>nul
mkdir .yellow_box_phish\traffic_logs 2>nul
mkdir .yellow_box_phish\phishing_templates 2>nul
mkdir .yellow_box_phish\captured_credentials 2>nul
mkdir .yellow_box_phish\ssh_keys 2>nul
mkdir .yellow_box_phish\ssh_logs 2>nul
mkdir .yellow_box_phish\time_history 2>nul
mkdir .yellow_box_phish\wordlists 2>nul
mkdir .yellow_box_phish\custom_phishing 2>nul
mkdir .yellow_box_phish\signal_session 2>nul
mkdir .yellow_box_phish\web_ui 2>nul
mkdir .yellow_box_phish\webhooks 2>nul

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          ✅ INSTALLATION COMPLETE!                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 To start YellowBoxPhish:
echo   python yellow_box_phish.py
echo.
echo 🌐 Web Interface:
echo   http://localhost:8080
echo.
echo 💡 Type 'help' for commands, 'exit' to quit
echo.
pause