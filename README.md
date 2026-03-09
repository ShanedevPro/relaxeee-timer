# Relax Timer

Relax Timer is a lightweight break reminder for focused work sessions, with both a command-line mode and a Windows-friendly desktop interface.

## Why It Exists

- Nudge yourself to step away from the keyboard before fatigue builds up.
- Use a minimal terminal timer when you want zero UI overhead.
- Switch to the desktop app when you want notifications, countdown visuals, and a simple focus/relax loop.

## Features

- Configurable reminder interval from the CLI
- Custom reminder message support
- Optional finite reminder counts for short sessions
- Windows toast notifications and system beep support
- Desktop GUI with focus and relax phases, countdown state, and visual customization

## Tech Stack

- Python
- Tkinter + CustomTkinter
- Windows notifications via PowerShell

## Quick Start

### CLI mode

```bash
python relax_timer.py
python relax_timer.py --interval 30
python relax_timer.py --count 4 --message "Stand up and stretch."
```

### Desktop mode (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\RelaxTimer.pyw
```

If you want a click-to-run workflow, double-click `RelaxTimer.bat`.

## Project Structure

- `relax_timer.py`: terminal-first reminder flow
- `RelaxTimer.pyw`: GUI desktop app for Windows
- `app_notifications.py`: notification helper
- `app_assets.py`: visual assets used by the GUI
- `scripts/`: helper scripts for running, building, and cleaning

## Packaging

To build a standalone Windows executable:

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name RelaxTimer RelaxTimer.pyw
```

Or use the included helper scripts:

- `.\scripts\build_exe.ps1`
- `.\scripts\run.ps1`
- `.\scripts\clean.ps1`

## Current Status

This repository is maintained as a compact productivity utility focused on local desktop use rather than cloud sync or team features.

## Public Review Note

- Public privacy reviews should verify that no notification tokens, personal reminder history, private screenshots, or local Windows user paths are committed.
