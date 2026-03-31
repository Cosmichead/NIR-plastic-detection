@echo off
setlocal
title Plastic Detector Builder

echo ===================================================
echo    🏗️  Plastic Detector Executable Builder
echo ===================================================

cd /d "%~dp0"

if not exist ".venv" (
    echo ❌ Virtual environment not found. Please run RUN_APP.bat first to set it up.
    pause
    exit /b
)

call .venv\Scripts\activate

echo 🔨 Building executable...
python build_executable.py

echo.
if exist "dist\PlasticDetector.exe" (
    echo ✅ Build successful!
    echo 📂 Executable is located in: dist\PlasticDetector.exe
) else (
    echo ❌ Build failed. Please check the output above for errors.
)
pause
