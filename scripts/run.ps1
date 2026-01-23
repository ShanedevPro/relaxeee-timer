$ErrorActionPreference = "Stop"

if (Test-Path ".\\dist\\RelaxTimer.exe") {
  & ".\\dist\\RelaxTimer.exe"
  exit $LASTEXITCODE
}

if (Test-Path ".\\.venv\\Scripts\\pythonw.exe") {
  & ".\\.venv\\Scripts\\pythonw.exe" ".\\RelaxTimer.pyw"
  exit $LASTEXITCODE
}

if (Get-Command pythonw -ErrorAction SilentlyContinue) {
  pythonw ".\\RelaxTimer.pyw"
  exit $LASTEXITCODE
}

throw "Could not find dist\\RelaxTimer.exe or pythonw to run the app. Create a venv and install requirements first."
