@echo off
REM CYCLOPUS - Windows Installation Script

echo ========================================
echo 🐙 CYCLOPUS Installation Script
echo ========================================
echo.

REM Check Python
echo [*] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 not found. Please install Python 3.8+
    echo [INFO] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check pip
echo [*] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] pip not found, installing...
    python -m ensurepip --upgrade
)

REM Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [*] Installing Python dependencies...
pip install -r requirements.txt

REM Install optional packages
echo [*] Installing optional packages...
pip install pyperclip pygetwindow pyautogui

REM Create directories
echo [*] Creating configuration directories...
mkdir .cyclopus 2>nul
mkdir .cyclopus\payloads 2>nul
mkdir .cyclopus\workspaces 2>nul
mkdir .cyclopus\reports 2>nul
mkdir .cyclopus\phishing_pages 2>nul
mkdir .cyclopus\captured_credentials 2>nul
mkdir .cyclopus\ssh_keys 2>nul
mkdir .cyclopus\traffic_logs 2>nul
mkdir .cyclopus\nikto_results 2>nul
mkdir .cyclopus\keylog_exfil 2>nul
mkdir .cyclopus\deployments 2>nul
mkdir .cyclopus\cracking 2>nul
mkdir .cyclopus\arp_logs 2>nul
mkdir .cyclopus\mac_logs 2>nul
mkdir .cyclopus\nat_logs 2>nul
mkdir .cyclopus\docker_scans 2>nul
mkdir .cyclopus\email_composer 2>nul
mkdir .cyclopus\pdf_reports 2>nul
mkdir cyclopus_reports 2>nul
mkdir logs 2>nul

REM Create .env file
if not exist .env (
    echo [*] Creating .env file...
    copy .env.example .env
)

REM Create run script
echo [*] Creating run script...
echo @echo off > cyclopus-run.bat
echo call venv\Scripts\activate.bat >> cyclopus-run.bat
echo python cyclopus.py %%* >> cyclopus-run.bat

echo.
echo ========================================
echo ✅ CYCLOPUS Installation Complete!
echo ========================================
echo.
echo 🚀 To start CYCLOPUS:
echo    cyclopus-run.bat
echo.
echo 🔍 To check requirements:
echo    python requirements-check.py
echo.
echo 🧪 To run tests:
echo    python commands-test.py
echo.
pause