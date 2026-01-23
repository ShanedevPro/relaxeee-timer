$ErrorActionPreference = "Stop"

Write-Host "Building RelaxTimer.exe with PyInstaller..." -ForegroundColor Cyan

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
  Write-Host "PyInstaller not found; installing..." -ForegroundColor Yellow
  python -m pip install --upgrade pyinstaller
}

pyinstaller --onefile --windowed --name RelaxTimer ".\\RelaxTimer.pyw"

Write-Host "Built: dist\\RelaxTimer.exe" -ForegroundColor Green
