@echo off
setlocal
cd /d "%~dp0"

REM Prefer a built EXE if present
if exist "%~dp0dist\RelaxTimer.exe" (
    start "" "%~dp0dist\RelaxTimer.exe"
    exit /b 0
)

REM Check if we have a virtual environment with required packages
if exist "%~dp0.venv\Scripts\pythonw.exe" (
    start "" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0RelaxTimer.pyw"
    exit /b 0
)

REM Fallback to system python
start "" pythonw "%~dp0RelaxTimer.pyw"
