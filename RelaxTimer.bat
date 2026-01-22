@echo off
setlocal
cd /d "%~dp0"

REM Check if we have a virtual environment with required packages
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "%~dp0RelaxTimer.pyw"
) else (
    REM Fallback to system python
    start "" pythonw "%~dp0RelaxTimer.pyw"
)
