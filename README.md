# Relax Timer

This tiny utility reminds you to take a short pause every few minutes. It prints the next reminder time, emits a terminal beep, and raises a Windows notification when available.

## Usage

```bash
python relax_timer.py          # remind every 25 minutes, forever
python relax_timer.py -i 30    # remind every 30 minutes
python relax_timer.py -n 3     # stop after three reminders
python relax_timer.py -m "Lie back and breathe"  # customize the headline message
```

## Windows click-to-run

If you want a simple "click to run" experience, use the GUI version:

- Double-click `RelaxTimer.pyw` to open the window.
- Or double-click `RelaxTimer.bat` (uses `pythonw` so no console window).

Set your interval, press Start, and Windows notifications will appear on schedule.

## GUI behavior

- Start switches into a focus view (big countdown + running animal).
- Stop returns to settings.
- The timer auto-switches between Focus and Relax (Pomodoro-style).

## Developer setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\RelaxTimer.pyw
```

## Build EXE (PyInstaller)

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name RelaxTimer RelaxTimer.pyw
```

## Tip

Let the script run in the background (a terminal tab or split) while you work. When the reminder fires, pause, step away from the keyboard, and stretch before resuming work.
