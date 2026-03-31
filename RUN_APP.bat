@echo off
cd /d "%~dp0"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 goto NoPython

if exist ".venv" goto VenvExists
echo Creating virtual environment...
python -m venv .venv
:VenvExists

echo Activating virtual environment...
call .venv\Scripts\activate

echo Checking dependencies...
python -c "import webview" >nul 2>&1
if errorlevel 1 goto InstallDeps
goto Launch

:InstallDeps
echo Installing dependencies...
pip install -r scripts/requirements.txt

:Launch
echo Starting application...
python desktop_app.py
if errorlevel 1 goto Error
goto End

:NoPython
echo Python is not installed or not in PATH.
pause
goto End

:Error
echo Application exited with error.
pause

:End
