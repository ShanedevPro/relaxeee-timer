$ErrorActionPreference = "Stop"

Write-Host "Cleaning build artifacts..." -ForegroundColor Cyan

$paths = @(
  "build",
  "dist",
  "__pycache__",
  "RelaxTimer.spec"
)

foreach ($p in $paths) {
  if (Test-Path $p) {
    Remove-Item -Recurse -Force $p
    Write-Host "Removed $p"
  }
}

Write-Host "Done." -ForegroundColor Green
