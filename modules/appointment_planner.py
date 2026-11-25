
"""Modern appointment planner for Urody."""

import calendar
from datetime import date, datetime, timedelta
import tkinter as tk

from services import SERVICES
from modules.appointment_logic import (
    calculate_duration,
    calculate_total,
    create_appointment,
    load_appointments,
    save_appointment,
    validate_appointment,
)


# URODY color palette
BG = "#F5F5F0"
GREEN = "#34483D"
GREEN_DARK = "#26372F"
TEXT = "#26332C"
MUTED = "#747B73"
WHITE = "#FFFFFF"
BORDER = "#E1E5DD"
SAGE = "#E9EEE8"
GOLD = "#B49A70"

SUCCESS_BG = "#EAF3EA"
SUCCESS_FG = "#326B45"
ERROR_BG = "#FCECEC"
ERROR_FG = "#9B3D4A"

MONTH_NAMES = (
    "Styczeń", "Luty", "Marzec", "Kwiecień",
    "Maj", "Czerwiec", "Lipiec", "Sierpień",
    "Wrzesień", "Październik", "Listopad", "Grudzień",
)

WEEKDAY_NAMES = ("Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd")


def next_workday(start_date):
    while start_date.weekday() >= 5:
        start_date += timedelta(days=1)
    return start_date


class AppointmentPlanner:

    def __init__(self, parent, on_saved=None):
        self.parent = parent
        self.on_saved = on_saved

        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True)

        self.service_vars = []
        self.selected_date = next_workday(
            date.today() + timedelta(days=1)
        )
        self.visible_month = self.selected_date.replace(day=1)
        self.selected_time = ""
        self.status_label = None

        self._build_page()
        self._render_calendar()
        self._render_time_choices()
        self._update_summary()

    # PAGE LAYOUT

    def _build_page(self):
        title_row = tk.Frame(self.frame, bg=BG)
        title_row.pack(fill="x", pady=(0, 18))

        tk.Label(
            title_row,
            text="Zaplanuj wizytę",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(side="left")

        tk.Label(
            title_row,
            text="Pon–Pt  ·  09:00–18:00",
            font=("Arial", 10, "bold"),
            bg=SAGE,
            fg=GREEN,
            padx=14,
            pady=9,
        ).pack(side="right")

        columns = tk.Frame(self.frame, bg=BG)
        columns.pack(fill="both", expand=True)

        columns.grid_columnconfigure(0, weight=3, minsize=220)
        columns.grid_columnconfigure(1, weight=4, minsize=290)
        columns.grid_columnconfigure(2, weight=3, minsize=210)
        columns.grid_rowconfigure(0, weight=1)

        self.service_card = self._create_card(
            columns, "Wybierz usługi"
        )
        self.service_card.grid(
            row=0, column=0, sticky="nsew", padx=(0, 7)
        )

        self.date_card = self._create_card(
            columns, "Wybierz termin"
        )
        self.date_card.grid(
            row=0, column=1, sticky="nsew", padx=7
        )

        self.summary_card = self._create_card(
            columns, "Podsumowanie wizyty"
        )
        self.summary_card.grid(
            row=0, column=2, sticky="nsew", padx=(7, 0)
        )

        self._build_service_choices()
        self._build_date_choices()
        self._build_summary()

    def _create_card(self, parent, title):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=14,
            pady=14,
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 13, "bold"),
            bg=WHITE,
            fg=GREEN,
        ).pack(anchor="w", pady=(0, 14))

        return card

    # SERVICE SELECTION

    def _build_service_choices(self):
        for service in SERVICES:
            variable = tk.BooleanVar(
                master=self.frame,
                value=False
            )

            self.service_vars.append((variable, service))

            item = tk.Frame(
                self.service_card,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
                padx=7,
                pady=7,
            )
            item.pack(fill="x", pady=5)

            tk.Checkbutton(
                item,
                text=service["name"],
                variable=variable,
                command=self._on_services_changed,
                font=("Arial", 10, "bold"),
                bg=WHITE,
                fg=TEXT,
                activebackground=WHITE,
                activeforeground=GREEN,
                selectcolor=SAGE,
                anchor="w",
                justify="left",
                wraplength=175,
                bd=0,
                highlightthickness=0,
                cursor="hand2",
            ).pack(fill="x", anchor="w")

            tk.Label(
                item,
                text=(
                    f"{service['price']} PLN  ·  "
                    f"{service['duration']} min"
                ),
                font=("Arial", 9),
                bg=WHITE,
                fg=MUTED,
            ).pack(anchor="w", padx=(24, 0), pady=(3, 0))

    # CALENDAR

    def _build_date_choices(self):
        month_row = tk.Frame(
            self.date_card,
            bg=WHITE
        )
        month_row.pack(fill="x", pady=(0, 12))

        self.previous_month_button = tk.Button(
            month_row,
            text="‹",
            command=lambda: self._change_month(-1),
            font=("Arial", 15, "bold"),
            bg=SAGE,
            fg=GREEN,
            activebackground=GREEN,
            activeforeground=WHITE,
            bd=0,
            width=3,
            cursor="hand2",
        )
        self.previous_month_button.pack(side="left")

        self.month_label = tk.Label(
            month_row,
            text="",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=TEXT,
        )
        self.month_label.pack(side="left", expand=True)

        tk.Button(
            month_row,
            text="›",
            command=lambda: self._change_month(1),
            font=("Arial", 15, "bold"),
            bg=SAGE,
            fg=GREEN,
            activebackground=GREEN,
            activeforeground=WHITE,
            bd=0,
            width=3,
            cursor="hand2",
        ).pack(side="right")

        self.calendar_grid = tk.Frame(
            self.date_card,
            bg=WHITE
        )
        self.calendar_grid.pack(fill="x", pady=(0, 12))

        self.date_caption = tk.Label(
            self.date_card,
            text="",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=GREEN,
        )
        self.date_caption.pack(anchor="w", pady=(0, 12))

        tk.Label(
            self.date_card,
            text="Dostępne godziny",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", pady=(2, 8))

        self.time_choices_frame = tk.Frame(
            self.date_card,
            bg=WHITE
        )
        self.time_choices_frame.pack(fill="x")

    def _change_month(self, offset):
        month_index = self.visible_month.month - 1 + offset
        year = self.visible_month.year + month_index // 12
        month = month_index % 12 + 1

        self.visible_month = date(year, month, 1)
        self._render_calendar()

    def _render_calendar(self):
        self.month_label.configure(
            text=(
                f"{MONTH_NAMES[self.visible_month.month - 1]} "
                f"{self.visible_month.year}"
            )
        )

        self.date_caption.configure(
            text=f"Wybrana data: {self.selected_date:%d.%m.%Y}"
        )

        for child in self.calendar_grid.winfo_children():
            child.destroy()

        for column, name in enumerate(WEEKDAY_NAMES):
            tk.Label(
                self.calendar_grid,
                text=name,
                font=("Arial", 8, "bold"),
                bg=WHITE,
                fg=MUTED,
                width=3,
            ).grid(
                row=0,
                column=column,
                padx=1,
                pady=(2, 6)
            )

        today = date.today()

        weeks = calendar.Calendar(
            firstweekday=0
        ).monthdayscalendar(
            self.visible_month.year,
            self.visible_month.month
        )

        for row, week in enumerate(weeks, start=1):
            for column, day_number in enumerate(week):

                if day_number == 0:
                    tk.Label(
                        self.calendar_grid,
                        text="",
                        bg=WHITE,
                        width=3
                    ).grid(
                        row=row,
                        column=column,
                        padx=1,
                        pady=1
                    )
                    continue

                current_day = date(
                    self.visible_month.year,
                    self.visible_month.month,
                    day_number
                )

                is_workday = current_day.weekday() < 5
                is_future = current_day >= today
                selected = current_day == self.selected_date

                button = tk.Button(
                    self.calendar_grid,
                    text=str(day_number),
                    command=lambda chosen=current_day:
                    self._select_date(chosen),
                    font=(
                        "Arial",
                        8,
                        "bold" if selected else "normal"
                    ),
                    bg=GREEN if selected else WHITE,
                    fg=(
                        WHITE if selected
                        else TEXT if is_workday and is_future
                        else "#B8BEB7"
                    ),
                    activebackground=GREEN_DARK,
                    activeforeground=WHITE,
                    disabledforeground="#B8BEB7",
                    bd=0,
                    width=3,
                    padx=1,
                    pady=5,
                    cursor=(
                        "hand2"
                        if is_workday and is_future
                        else "arrow"
                    ),
                    state=(
                        "normal"
                        if is_workday and is_future
                        else "disabled"
                    ),
                )

                button.grid(
                    row=row,
                    column=column,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )

        self._render_time_choices()

    def _select_date(self, selected_date):
        self.selected_date = selected_date
        self.selected_time = ""

        self._clear_status()
        self._render_calendar()
        self._update_summary()

    # SERVICE AND TIME LOGIC

    def _on_services_changed(self):
        self.selected_time = ""

        self._clear_status()
        self._render_time_choices()
        self._update_summary()

    def _selected_services(self):
        return [
            service
            for variable, service in self.service_vars
            if variable.get()
        ]

    def _render_time_choices(self):
        for child in self.time_choices_frame.winfo_children():
            child.destroy()

        selected_services = self._selected_services()

        if not selected_services:
            self.selected_time = ""

            tk.Label(
                self.time_choices_frame,
                text="Wybierz usługi, aby zobaczyć wolne terminy.",
                font=("Arial", 9),
                bg=WHITE,
                fg=MUTED,
                wraplength=230,
                justify="left",
            ).pack(anchor="w")

            return

        try:
            appointments = load_appointments()

        except (OSError, ValueError) as error:
            self.selected_time = ""

            self._set_status(
                f"Nie można wczytać wizyt: {error}",
                error=True
            )

            tk.Label(
                self.time_choices_frame,
                text="Terminy są chwilowo niedostępne.",
                font=("Arial", 9),
                bg=WHITE,
                fg=ERROR_FG,
                wraplength=230,
                justify="left",
            ).pack(anchor="w")

            return

        available_times = []

        for minute_of_day in range(9 * 60, 18 * 60, 30):
            hour, minute = divmod(minute_of_day, 60)
            candidate_time = f"{hour:02d}:{minute:02d}"

            if validate_appointment(
                    selected_services,
                    self.selected_date.strftime("%d.%m.%Y"),
                    candidate_time,
                    appointments,
            ) is None:
                available_times.append(candidate_time)

        if self.selected_time not in available_times:
            self.selected_time = ""

        if not available_times:
            tk.Label(
                self.time_choices_frame,
                text="Brak wolnych godzin dla wybranych usług i daty.",
                font=("Arial", 9),
                bg=WHITE,
                fg=MUTED,
                wraplength=230,
                justify="left",
            ).pack(anchor="w")

            return

        for index, candidate_time in enumerate(available_times):
            selected = candidate_time == self.selected_time

            button = tk.Button(
                self.time_choices_frame,
                text=candidate_time,
                command=lambda chosen=candidate_time:
                self._select_time(chosen),
                font=("Arial", 9, "bold"),
                bg=GREEN if selected else SAGE,
                fg=WHITE if selected else GREEN,
                activebackground=GREEN_DARK,
                activeforeground=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
                bd=0,
                padx=5,
                pady=7,
                cursor="hand2",
            )

            button.grid(
                row=index // 3,
                column=index % 3,
                padx=3,
                pady=3,
                sticky="nsew"
            )

        for column in range(3):
            self.time_choices_frame.grid_columnconfigure(
                column,
                weight=1
            )

    def _select_time(self, selected_time):
        self.selected_time = selected_time

        self._clear_status()
        self._render_time_choices()
        self._update_summary()

    # APPOINTMENT SUMMARY

    def _build_summary(self):
        self.summary_services = tk.Label(
            self.summary_card,
            text="Nie wybrano usług.",
            font=("Arial", 9),
            bg=WHITE,
            fg=MUTED,
            justify="left",
            anchor="nw",
            wraplength=185,
        )
        self.summary_services.pack(fill="x", anchor="w")

        tk.Frame(
            self.summary_card,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=12)

        self.summary_date = tk.Label(
            self.summary_card,
            text="Data: —",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT,
            anchor="w",
            justify="left",
        )
        self.summary_date.pack(fill="x", pady=3)

        self.summary_time = tk.Label(
            self.summary_card,
            text="Godzina: —",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT,
            anchor="w",
            justify="left",
        )
        self.summary_time.pack(fill="x", pady=3)

        self.summary_duration = tk.Label(
            self.summary_card,
            text="Czas: —",
            font=("Arial", 9),
            bg=WHITE,
            fg=TEXT,
            anchor="w",
            justify="left",
        )
        self.summary_duration.pack(fill="x", pady=3)

        self.summary_total = tk.Label(
            self.summary_card,
            text="Łącznie: 0 PLN",
            font=("Arial", 14, "bold"),
            bg=WHITE,
            fg=GREEN,
            anchor="w",
        )
        self.summary_total.pack(fill="x", pady=(12, 14))

        self.save_button = tk.Button(
            self.summary_card,
            text="Zapisz wizytę",
            command=self.save_current_appointment,
            font=("Arial", 10, "bold"),
            bg=GREEN,
            fg=WHITE,
            activebackground=GREEN_DARK,
            activeforeground=WHITE,
            disabledforeground="#9CA59B",
            bd=0,
            padx=10,
            pady=12,
            cursor="hand2",
            state="disabled",
        )
        self.save_button.pack(fill="x")

        self.status_label = tk.Label(
            self.summary_card,
            text="",
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=MUTED,
            wraplength=185,
            justify="left",
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(10, 0))

    def _update_summary(self):
        selected_services = self._selected_services()

        if selected_services:
            self.summary_services.configure(
                text="\n".join(
                    f"{service['name']} — "
                    f"{service['price']} PLN — "
                    f"{service['duration']} min"
                    for service in selected_services
                )
            )

            total = calculate_total(selected_services)
            duration = calculate_duration(selected_services)

        else:
            self.summary_services.configure(
                text="Nie wybrano usług."
            )
            total = 0
            duration = 0

        self.summary_date.configure(
            text=f"Data: {self.selected_date:%d.%m.%Y}"
        )

        if self.selected_time and duration:
            end_time = (
                    datetime.strptime(
                        self.selected_time,
                        "%H:%M"
                    )
                    + timedelta(minutes=duration)
            ).strftime("%H:%M")

            self.summary_time.configure(
                text=f"Godzina: {self.selected_time}–{end_time}"
            )

        else:
            self.summary_time.configure(
                text="Godzina: wybierz termin"
            )

        self.summary_duration.configure(
            text=(
                f"Czas: {duration} min"
                if duration
                else "Czas: —"
            )
        )

        self.summary_total.configure(
            text=f"Łącznie: {total} PLN"
        )

        appointment = None

        if selected_services and self.selected_time:
            appointment = create_appointment(
                selected_services,
                self.selected_date.strftime("%d.%m.%Y"),
                self.selected_time,
            )

        self.save_button.configure(
            state="normal" if appointment else "disabled"
        )

    # STATUS MESSAGES

    def _set_status(self, text, *, error=False, success=False):
        background = (
            SUCCESS_BG if success
            else ERROR_BG if error
            else WHITE
        )

        foreground = (
            SUCCESS_FG if success
            else ERROR_FG if error
            else MUTED
        )

        self.status_label.configure(
            text=text,
            bg=background,
            fg=foreground,
            padx=8,
            pady=8,
        )

    def _clear_status(self):
        self.status_label.configure(
            text="",
            bg=WHITE,
            padx=0,
            pady=0
        )

    # SAVE APPOINTMENT

    def save_current_appointment(self):
        selected_services = self._selected_services()
        selected_date = self.selected_date.strftime("%d.%m.%Y")

        try:
            appointments = load_appointments()

            error = validate_appointment(
                selected_services,
                selected_date,
                self.selected_time,
                appointments,
            )

            if error:
                self._set_status(error, error=True)
                self.save_button.configure(state="disabled")
                self._render_time_choices()
                return

            appointment = create_appointment(
                selected_services,
                selected_date,
                self.selected_time,
                appointments,
            )

            save_appointment(appointment)

        except (OSError, ValueError) as error:
            self._set_status(str(error), error=True)
            self._render_time_choices()
            self._update_summary()
            return

        if self.on_saved:
            self.on_saved(appointment)
        else:
            self._set_status(
                "Wizyta została zapisana.",
                success=True
            )
