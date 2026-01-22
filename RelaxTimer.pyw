#!/usr/bin/env pythonw
"""
Simple Windows-friendly relax timer with notifications.
"""

import datetime
import tkinter as tk
import customtkinter as ctk
import random
from typing import Optional

from app_assets import ANIMALS, PALETTES
from app_notifications import send_notification

# terminal style constants
TERMINAL_BG = "#0C0C0C"
TERMINAL_FG = "#33FF33"  # Bright green
TERMINAL_FONT = ("Consolas", 14)
TERMINAL_FONT_BOLD = ("Consolas", 14, "bold")
TITLE_FONT = ("Consolas", 24, "bold")
COUNTDOWN_FONT = ("Consolas", 40, "bold")



class RelaxTimerApp:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("Relax Timer")
        self.root.geometry("520x640")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # Pomodoro-style durations (minutes)
        self.focus_minutes_var = tk.StringVar(value="25")
        self.break_minutes_var = tk.StringVar(value="5")
        self.message_var = tk.StringVar(
            value="Take a breath and stretch for a couple of minutes."
        )
        self.status_var = tk.StringVar(value="Idle. Set your interval and press Start.")
        self.focus_status_var = tk.StringVar(value="Next reminder in 25:00.")
        self.countdown_var = tk.StringVar(value="25:00")
        self.phase_var = tk.StringVar(value="FOCUS")
        self.cute_mode_var = tk.BooleanVar(value=False)
        self.animal_var = tk.StringVar(value="cat")
        self.palette_var = tk.StringVar(value="Emerald")

        self.current_animal = "cat"
        self.animation_step = 0
        self.animation_id: Optional[str] = None
        self.runner_id: Optional[int] = None
        self.runner_x = -200
        self.runner_speed = 2

        self.running = False
        self.focus_minutes = 25.0
        self.break_minutes = 5.0
        self.phase: str = "focus"  # "focus" | "break"
        self.next_fire: Optional[datetime.datetime] = None
        self.timer_id: Optional[str] = None
        self.is_focus_view = False

        self._build_ui()
        self._apply_palette(self.palette_var.get())
        self._schedule_status_update()

    def _build_ui(self) -> None:
        self.root.configure(fg_color=TERMINAL_BG)

        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=2,
            fg_color="#1a1a1a",
            border_width=2,
            border_color=TERMINAL_FG,
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="> Relax_Timer.exe",
            font=TITLE_FONT,
            text_color=TERMINAL_FG,
        )
        self.title_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Running system checks... Reminding user to pause.",
            font=TERMINAL_FONT,
            text_color=TERMINAL_FG,
        )
        self.desc_label.pack(anchor="w", padx=20, pady=(0, 20))

        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_frame.pack(fill="x", padx=20)

        self.focus_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.focus_frame.pack_forget()

        self.runner_canvas = tk.Canvas(
            self.focus_frame,
            height=140,
            highlightthickness=0,
            bg=TERMINAL_BG,
        )
        self.runner_canvas.pack(fill="x", padx=20, pady=(0, 10))

        self.countdown_label = ctk.CTkLabel(
            self.focus_frame,
            textvariable=self.countdown_var,
            font=COUNTDOWN_FONT,
            text_color=TERMINAL_FG,
        )
        self.countdown_label.pack(anchor="center", pady=(10, 5))

        self.phase_label = ctk.CTkLabel(
            self.focus_frame,
            textvariable=self.phase_var,
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=TERMINAL_FG,
        )
        self.phase_label.pack(anchor="center", pady=(0, 5))

        self.focus_status_label = ctk.CTkLabel(
            self.focus_frame,
            textvariable=self.focus_status_var,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=TERMINAL_FG,
        )
        self.focus_status_label.pack(anchor="center", pady=(0, 15))

        focus_button_frame = ctk.CTkFrame(self.focus_frame, fg_color="transparent")
        focus_button_frame.pack(fill="x", pady=(10, 10))

        self.focus_stop_btn = ctk.CTkButton(
            focus_button_frame,
            text="[ STOP ]",
            command=self.stop,
            width=120,
            height=35,
            font=TERMINAL_FONT_BOLD,
            fg_color=TERMINAL_FG,
            text_color="black",
            hover_color="#28CC28",
        )
        self.focus_stop_btn.pack(side="top", pady=(0, 10))

        form_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        form_frame.pack(fill="x")

        self.interval_label = ctk.CTkLabel(
            form_frame,
            text="Focus (min):",
            font=TERMINAL_FONT,
            text_color=TERMINAL_FG,
        )
        self.interval_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.interval_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.focus_minutes_var,
            width=100,
            placeholder_text="25",
            font=TERMINAL_FONT,
            fg_color="transparent",
            border_color=TERMINAL_FG,
            text_color=TERMINAL_FG,
        )
        self.interval_entry.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

        self.break_label = ctk.CTkLabel(
            form_frame,
            text="Relax (min):",
            font=TERMINAL_FONT,
            text_color=TERMINAL_FG,
        )
        self.break_label.grid(row=0, column=2, sticky="w", padx=(18, 0), pady=(0, 5))

        self.break_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.break_minutes_var,
            width=90,
            placeholder_text="5",
            font=TERMINAL_FONT,
            fg_color="transparent",
            border_color=TERMINAL_FG,
            text_color=TERMINAL_FG,
        )
        self.break_entry.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=(0, 5))

        self.message_label = ctk.CTkLabel(
            form_frame,
            text="Message:",
            font=TERMINAL_FONT,
            text_color=TERMINAL_FG,
        )
        self.message_label.grid(row=1, column=0, sticky="w", pady=(15, 5))

        self.message_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.message_var,
            width=300,
            placeholder_text="Enter custom message...",
            font=TERMINAL_FONT,
            fg_color="transparent",
            border_color=TERMINAL_FG,
            text_color=TERMINAL_FG,
        )
        self.message_entry.grid(
            row=1, column=1, columnspan=3, sticky="w", padx=(10, 0), pady=(15, 5)
        )

        self.animal_label = ctk.CTkLabel(
            form_frame,
            text="Animal runner:",
            font=TERMINAL_FONT,
            text_color=TERMINAL_FG,
        )
        self.animal_label.grid(row=2, column=0, sticky="w", pady=(15, 5))

        self.animal_picker = ctk.CTkOptionMenu(
            form_frame,
            values=list(ANIMALS.keys()),
            variable=self.animal_var,
            command=self._set_animal,
            fg_color=PALETTES["Emerald"]["panel"],
            button_color=TERMINAL_FG,
            button_hover_color="#28CC28",
            text_color=TERMINAL_FG,
            dropdown_fg_color="#1a1a1a",
            dropdown_text_color=TERMINAL_FG,
        )
        self.animal_picker.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(15, 5))

        self.palette_label = ctk.CTkLabel(
            form_frame,
            text="Color style:",
            font=TERMINAL_FONT,
            text_color=TERMINAL_FG,
        )
        self.palette_label.grid(row=3, column=0, sticky="w", pady=(15, 5))

        palette_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        palette_frame.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(15, 5))

        self.palette_buttons = []
        for name, palette in PALETTES.items():
            btn = ctk.CTkButton(
                palette_frame,
                text="",
                width=26,
                height=26,
                fg_color=palette["accent"],
                hover_color=palette["fg"],
                corner_radius=4,
                command=lambda n=name: self._apply_palette(n),
            )
            btn.pack(side="left", padx=(0, 6))
            self.palette_buttons.append(btn)

        self.cute_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Runner [ON/OFF]",
            variable=self.cute_mode_var,
            command=self._toggle_cute_mode,
            font=TERMINAL_FONT,
            progress_color=TERMINAL_FG,
            fg_color="gray30",
            button_color="gray80",
            text_color=TERMINAL_FG,
        )
        self.cute_switch.pack(anchor="w", pady=(15, 0))

        button_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=30)

        self.start_btn = ctk.CTkButton(
            button_frame,
            text="[ EXECUTE ]",
            command=self.start,
            width=120,
            height=35,
            font=TERMINAL_FONT_BOLD,
            fg_color=TERMINAL_FG,
            text_color="black",
            hover_color="#28CC28",
        )
        self.start_btn.pack(side="left")

        self.status_label = ctk.CTkLabel(
            self.settings_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=TERMINAL_FG,
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

    def start(self) -> None:
        try:
            focus_minutes = float(self.focus_minutes_var.get().strip())
            break_minutes = float(self.break_minutes_var.get().strip())
        except ValueError:
            self.status_var.set("Please enter valid numbers for focus/relax minutes.")
            return
        if focus_minutes <= 0 or break_minutes <= 0:
            self.status_var.set("Focus/relax minutes must be greater than zero.")
            return

        self.focus_minutes = focus_minutes
        self.break_minutes = break_minutes
        self.running = True
        self._set_phase("focus")

        self.start_btn.configure(state="disabled")
        self.status_var.set("Timer running...")
        self._show_focus_view(True)

        self._schedule_next_reminder()

    def stop(self) -> None:
        self.running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.next_fire = None
        self._set_phase("focus")

        self.start_btn.configure(state="normal")
        self.status_var.set("Timer stopped.")
        self._show_focus_view(False)

    def _toggle_cute_mode(self) -> None:
        if self.cute_mode_var.get():
            if not self.animal_var.get():
                self.animal_var.set("cat")
            self.current_animal = self.animal_var.get()
            if self.is_focus_view:
                self._start_runner()
        else:
            if self.animation_id:
                self.root.after_cancel(self.animation_id)
                self.animation_id = None
            self.runner_canvas.delete("all")

    def _set_animal(self, selection: str) -> None:
        self.current_animal = selection
        self.animal_var.set(selection)
        if self.cute_mode_var.get() and self.is_focus_view:
            self._start_runner()

    def _schedule_next_reminder(self) -> None:
        if not self.running or self.next_fire is None:
            return
        delay_seconds = max(
            0.0, (self.next_fire - datetime.datetime.now()).total_seconds()
        )
        self.timer_id = self.root.after(int(delay_seconds * 1000), self._fire_reminder)

    def _fire_reminder(self) -> None:
        if not self.running:
            return
        if self.phase == "focus":
            message = self.message_var.get().strip() or "Time to relax."
            send_notification("Relax Timer", f"Focus finished. {message}")
            self._set_phase("break")
        else:
            send_notification("Relax Timer", "Relax finished. Back to focus.")
            self._set_phase("focus")
        self._schedule_next_reminder()

    def _schedule_status_update(self) -> None:
        self._update_status()
        self.root.after(1000, self._schedule_status_update)

    def _update_status(self) -> None:
        if not self.running or self.next_fire is None:
            self.countdown_var.set("--:--")
            self.focus_status_var.set("Timer paused.")
            return
        remaining = self.next_fire - datetime.datetime.now()
        seconds_left = max(0, int(remaining.total_seconds()))
        minutes, seconds = divmod(seconds_left, 60)
        self.countdown_var.set(f"{minutes:02d}:{seconds:02d}")
        next_at = self.next_fire.strftime("%H:%M:%S")
        if self.phase == "focus":
            self.focus_status_var.set(f"Focus ends at {next_at}.")
        else:
            self.focus_status_var.set(f"Relax ends at {next_at}.")

    def _apply_palette(self, name: str) -> None:
        palette = PALETTES.get(name, PALETTES["Emerald"])
        self.palette_var.set(name)
        self.root.configure(fg_color=palette["bg"])
        self.main_frame.configure(fg_color=palette["panel"], border_color=palette["fg"])
        self.runner_canvas.configure(bg=palette["canvas"])

        self.title_label.configure(text_color=palette["fg"])
        self.desc_label.configure(text_color=palette["fg"])
        self.interval_label.configure(text_color=palette["fg"])
        self.break_label.configure(text_color=palette["fg"])
        self.message_label.configure(text_color=palette["fg"])
        self.animal_label.configure(text_color=palette["fg"])
        self.palette_label.configure(text_color=palette["fg"])
        self.status_label.configure(text_color=palette["fg"])
        self.countdown_label.configure(text_color=palette["fg"])
        self.phase_label.configure(text_color=palette["fg"])
        self.focus_status_label.configure(text_color=palette["fg"])

        self.interval_entry.configure(border_color=palette["fg"], text_color=palette["fg"])
        self.break_entry.configure(border_color=palette["fg"], text_color=palette["fg"])
        self.message_entry.configure(border_color=palette["fg"], text_color=palette["fg"])

        self.cute_switch.configure(
            progress_color=palette["fg"],
            text_color=palette["fg"],
            button_color=palette["fg"],
        )

        self.start_btn.configure(fg_color=palette["fg"], hover_color=palette["accent"])
        self.focus_stop_btn.configure(fg_color=palette["fg"], hover_color=palette["accent"])

        self.animal_picker.configure(
            button_color=palette["fg"],
            button_hover_color=palette["accent"],
            text_color=palette["fg"],
            dropdown_text_color=palette["fg"],
            dropdown_fg_color=palette["panel"],
            fg_color=palette["panel"],
        )

        for name, btn in zip(PALETTES.keys(), self.palette_buttons):
            btn.configure(
                fg_color=PALETTES[name]["accent"],
                hover_color=PALETTES[name]["fg"],
            )

        if self.cute_mode_var.get() and self.is_focus_view:
            self._start_runner()

    def _show_focus_view(self, enabled: bool) -> None:
        if enabled == self.is_focus_view:
            return
        self.is_focus_view = enabled
        if enabled:
            self.settings_frame.pack_forget()
            self.focus_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
            if not self.cute_mode_var.get():
                self.cute_mode_var.set(True)
            self._start_runner()
        else:
            self.focus_frame.pack_forget()
            self.settings_frame.pack(fill="x", padx=20)
            if self.animation_id:
                self.root.after_cancel(self.animation_id)
                self.animation_id = None
            self.runner_canvas.delete("all")

    def _estimate_animal_width(self, art: str) -> int:
        lines = art.splitlines()
        longest = max(len(line) for line in lines) if lines else 10
        return max(80, longest * 8)

    def _start_runner(self) -> None:
        self.runner_canvas.delete("all")
        self.animation_step = 0
        self.runner_x = -self._estimate_animal_width(ANIMALS[self.current_animal][0])
        self.runner_id = self.runner_canvas.create_text(
            self.runner_x,
            10,
            anchor="nw",
            text=ANIMALS[self.current_animal][0],
            font=("Courier New", 12, "bold"),
            fill=PALETTES.get(self.palette_var.get(), PALETTES["Emerald"])["fg"],
        )
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        self._animate_runner()

    def _animate_runner(self) -> None:
        if not self.cute_mode_var.get() or self.runner_id is None:
            return
        frames = ANIMALS[self.current_animal]
        self.animation_step = (self.animation_step + 1) % len(frames)
        self.runner_canvas.itemconfig(self.runner_id, text=frames[self.animation_step])
        self.runner_x += self.runner_speed
        canvas_width = self.runner_canvas.winfo_width() or 440
        if self.runner_x > canvas_width + 20:
            self.runner_x = -self._estimate_animal_width(frames[0])
        self.runner_canvas.coords(self.runner_id, self.runner_x, 10)
        self.animation_id = self.root.after(60, self._animate_runner)

    def _set_phase(self, phase: str) -> None:
        self.phase = phase
        if phase == "focus":
            self.phase_var.set("FOCUS")
            self.runner_speed = 2
            self.next_fire = datetime.datetime.now() + datetime.timedelta(
                minutes=self.focus_minutes
            )
        else:
            self.phase_var.set("RELAX")
            self.runner_speed = 1
            self.next_fire = datetime.datetime.now() + datetime.timedelta(
                minutes=self.break_minutes
            )


def main() -> None:
    root = ctk.CTk()
    app = RelaxTimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
