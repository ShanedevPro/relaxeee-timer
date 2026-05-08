#!/usr/bin/env python3
"""
Lightweight timer that reminds you to relax at a configurable cadence.
"""

import argparse
import datetime
import subprocess
import sys
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a simple work/break timer that nudges you every N minutes."
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=25.0,
        help="Minutes between reminders (default: 25).",
    )
    parser.add_argument(
        "-m",
        "--message",
        default="Take a breath and stretch for a couple of minutes.",
        help="Text to show when the reminder fires.",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=0,
        help="Number of reminders to emit before stopping (0 = infinite).",
    )
    return parser.parse_args()


def announce(message: str) -> None:
    """Deliver a short visual/audio cue that a break has arrived."""
    print("\n" + "=" * 60)
    print(message)
    print("=" * 60 + "\n")
    if sys.platform == "win32":
        send_notification("Relax Timer", message)
    print("\a", end="", flush=True)
    if sys.platform == "win32":
        try:
            import winsound

            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except ImportError:
            pass


def _ps_escape(text: str) -> str:
    return text.replace("'", "''")


def send_notification(title: str, message: str) -> None:
    if sys.platform != "win32":
        return
    title = _ps_escape(title)
    message = _ps_escape(message)
    ps_script = f"""
$ErrorActionPreference = 'SilentlyContinue'
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
$xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
$textNodes = $xml.GetElementsByTagName('text')
$textNodes.Item(0).AppendChild($xml.CreateTextNode('{title}')) | Out-Null
$textNodes.Item(1).AppendChild($xml.CreateTextNode('{message}')) | Out-Null
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Relax Timer')
$notifier.Show($toast)
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True,
        text=True,
        check=False,
    )


def format_next(target: datetime.datetime) -> str:
    return target.strftime("%H:%M:%S")


def main() -> None:
    args = parse_args()
    interval_minutes = max(0.1, args.interval)
    interval_seconds = interval_minutes * 60
    print(f"Relax timer starting: reminding every {interval_minutes:.1f} minutes.")
    if args.count:
        print(f"Will stop after {args.count} reminder(s). Ctrl+C to cancel early.")
    else:
        print("Press Ctrl+C to stop whenever you like.")

    reminder_number = 0
    try:
        while args.count == 0 or reminder_number < args.count:
            reminder_number += 1
            next_target = datetime.datetime.now() + datetime.timedelta(seconds=interval_seconds)
            print(
                f"[{reminder_number}] Next reminder at {format_next(next_target)} "
                f"({interval_minutes:.1f} min interval)."
            )
            time.sleep(interval_seconds)
            announce(args.message)
    except KeyboardInterrupt:
        print("\nTimer interrupted; have a relaxing rest of your day.")


if __name__ == "__main__":
    main()
