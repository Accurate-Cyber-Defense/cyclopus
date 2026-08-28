@echo off
REM CYCLOPUS - Windows Uninstall Script

echo ========================================
echo 🐙 CYCLOPUS Uninstall Script
echo ========================================
echo.

set /p confirm="Are you sure you want to uninstall CYCLOPUS? (y/N): "
if /i not "%confirm%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo [*] Removing CYCLOPUS...

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat 2>nul

REM Remove virtual environment
if exist venv (
    echo [*] Removing virtual environment...
    rmdir /s /q venv
)

REM Remove configuration
if exist .cyclopus (
    echo [*] Removing configuration...
    rmdir /s /q .cyclopus
)

REM Remove reports
if exist cyclopus_reports (
    echo [*] Removing reports...
    rmdir /s /q cyclopus_reports
)

REM Remove logs
if exist logs (
    echo [*] Removing logs...
    rmdir /s /q logs
)

REM Remove executable
if exist cyclopus-run.bat (
    echo [*] Removing executable...
    del cyclopus-run.bat
)

REM Remove .env
if exist .env (
    echo [*] Removing .env...
    del .env
)

REM Clean up Python cache
echo [*] Cleaning up...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s *.pyc 2>nul

echo.
echo ✅ CYCLOPUS uninstalled successfully!
pause