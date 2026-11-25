
"""Single-window Urody salon application."""

from datetime import datetime, timedelta
import tkinter as tk

from calculator import open_calculator
from modules.appointment_logic import load_appointments
from modules.appointment_planner import AppointmentPlanner
from services import SERVICES


# Modern salon color palette
BG = "#F5F5F0"
GREEN = "#34483D"
GREEN_DARK = "#26372F"
TEXT = "#26332C"
MUTED = "#747B73"
WHITE = "#FFFFFF"
BORDER = "#E1E5DD"

SUCCESS_BG = "#EAF3EA"
SUCCESS_FG = "#326B45"
ERROR_BG = "#FCECEC"
ERROR_FG = "#9B3D4A"


class UrodyApp:

    NAV_ITEMS = (
        ("home", "Strona główna"),
        ("services", "Katalog usług"),
        ("calculator", "Kalkulator cen"),
        ("planner", "Planer wizyty"),
        ("guide", "Poradnik"),
        ("about", "O salonie"),
    )

    def __init__(self, root):
        self.root = root
        self.root.title("URODY — Salon Kosmetyczny")
        self.root.geometry("1180x760")
        self.root.minsize(1020, 690)
        self.root.configure(bg=BG)

        self.current_page = "home"
        self.flash_message = ""
        self.nav_buttons = {}

        self.create_header()
        self.create_shell()
        self.show_page("home")

    # HEADER

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg=GREEN,
            height=90
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="URODY",
            font=("Arial", 27, "bold"),
            bg=GREEN,
            fg=WHITE,
        ).pack(anchor="w", padx=28, pady=(13, 0))

        tk.Label(
            header,
            text="SALON KOSMETYCZNY",
            font=("Arial", 10, "bold"),
            bg=GREEN,
            fg="#DCE5DC",
        ).pack(anchor="w", padx=31, pady=(0, 8))

    # MAIN LAYOUT

    def create_shell(self):
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True)

        sidebar = tk.Frame(
            shell,
            bg=WHITE,
            width=220
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="MENU",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=MUTED,
        ).pack(anchor="w", padx=20, pady=(24, 12))

        for page, label in self.NAV_ITEMS:

            button = tk.Label(
                sidebar,
                text=label,
                font=("Arial", 11, "bold"),
                anchor="w",
                padx=16,
                pady=13,
                bg=WHITE,
                fg=TEXT,
                cursor="hand2",
            )

            button.pack(fill="x", padx=10, pady=3)

            button.bind(
                "<Button-1>",
                lambda event, selected=page:
                self.show_page(selected)
            )

            button.bind(
                "<Enter>",
                lambda event, item=button:
                self._nav_hover(item, True)
            )

            button.bind(
                "<Leave>",
                lambda event, item=button:
                self._nav_hover(item, False)
            )

            self.nav_buttons[page] = button

        self.page_area = tk.Frame(shell, bg=BG)
        self.page_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.page_container = tk.Frame(
            self.page_area,
            bg=BG
        )
        self.page_container.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=22
        )

    # NAVIGATION

    def _nav_hover(self, button, hovering):
        if button.cget("bg") == GREEN:
            return

        button.configure(
            bg="#E9EEE8" if hovering else WHITE
        )

    def _set_navigation_state(self):
        for page, button in self.nav_buttons.items():

            selected = page == self.current_page

            button.configure(
                bg=GREEN if selected else WHITE,
                fg=WHITE if selected else TEXT,
            )

    def _clear_page(self):
        for child in self.page_container.winfo_children():
            child.destroy()

    def show_page(self, page):
        self.current_page = page

        self._set_navigation_state()
        self._clear_page()

        pages = {
            "home": self.show_home_page,
            "services": self.show_services,
            "calculator": self.show_calculator,
            "planner": self.show_planner,
            "guide": self.show_guide,
            "about": self.show_about,
        }

        pages[page]()

    # COMMON ELEMENTS

    def _page_heading(self, title, subtitle=""):
        tk.Label(
            self.page_container,
            text=title,
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 5))

        if subtitle:
            tk.Label(
                self.page_container,
                text=subtitle,
                font=("Arial", 10),
                bg=BG,
                fg=MUTED,
            ).pack(anchor="w", pady=(0, 18))

    def _card(self, parent, padding=18):
        return tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=padding,
            pady=padding,
        )

    def _inline_banner(self, parent, text, error=False):
        tk.Label(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            bg=ERROR_BG if error else SUCCESS_BG,
            fg=ERROR_FG if error else SUCCESS_FG,
            padx=12,
            pady=10,
            anchor="w",
            justify="left",
            wraplength=760,
        ).pack(fill="x", pady=(0, 14))

    def _action_button(self, parent, label, command):
        return tk.Button(
            parent,
            text=label,
            command=command,
            font=("Arial", 10, "bold"),
            bg=GREEN,
            fg=WHITE,
            activebackground=GREEN_DARK,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=12,
            cursor="hand2",
        )

    # HOME PAGE

    def show_home_page(self):
        self._page_heading(
            "Witamy w salonie Urody!",
            "Wybierz funkcję lub sprawdź najbliższą zaplanowaną wizytę."
        )

        if self.flash_message:
            self._inline_banner(
                self.page_container,
                self.flash_message
            )
            self.flash_message = ""

        card = self._card(
            self.page_container,
            padding=22
        )
        card.pack(fill="x", pady=(0, 16))

        tk.Label(
            card,
            text="Najbliższa wizyta",
            font=("Arial", 16, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 12))

        appointment, storage_error = self._next_appointment()

        if storage_error:
            tk.Label(
                card,
                text=f"Nie udało się wczytać zapisanych wizyt: {storage_error}",
                font=("Arial", 10),
                bg=WHITE,
                fg=ERROR_FG,
                wraplength=700,
                justify="left",
            ).pack(anchor="w")

        elif appointment is None:
            tk.Label(
                card,
                text="Brak zaplanowanych wizyt.",
                font=("Arial", 11),
                bg=WHITE,
                fg=MUTED,
            ).pack(anchor="w")

        else:
            service_names = ", ".join(
                service.get("name", "Usługa")
                for service in appointment["services"]
                if isinstance(service, dict)
            )

            end_time = appointment["start"] + timedelta(
                minutes=appointment["data"].get(
                    "total_duration", 0
                )
            )

            tk.Label(
                card,
                text=(
                    f"{appointment['start']:%d.%m.%Y}  •  "
                    f"{appointment['start']:%H:%M}–{end_time:%H:%M}"
                ),
                font=("Arial", 13, "bold"),
                bg=WHITE,
                fg=TEXT,
            ).pack(anchor="w")

            tk.Label(
                card,
                text=(
                    f"{service_names}  ·  "
                    f"{appointment['data'].get('total_price', 0)} PLN"
                ),
                font=("Arial", 11),
                bg=WHITE,
                fg=MUTED,
            ).pack(anchor="w", pady=(5, 0))

        self._action_button(
            self.page_container,
            "Zaplanuj wizytę",
            lambda: self.show_page("planner"),
        ).pack(anchor="w", pady=(0, 22))

        tk.Label(
            self.page_container,
            text="Nasze funkcje",
            font=("Arial", 16, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 12))

        actions = tk.Frame(
            self.page_container,
            bg=BG
        )
        actions.pack(fill="x")

        for page, label in self.NAV_ITEMS[1:4]:
            self._action_button(
                actions,
                label,
                lambda selected=page: self.show_page(selected),
            ).pack(side="left", padx=(0, 10))

    # APPOINTMENT DATA

    def _next_appointment(self):
        try:
            appointments = load_appointments()
        except (OSError, ValueError) as error:
            return None, str(error)

        now = datetime.now().replace(
            second=0,
            microsecond=0
        )

        upcoming = []

        for appointment in appointments:
            if not isinstance(appointment, dict):
                continue

            try:
                start = datetime.strptime(
                    f"{appointment['date']} {appointment['time']}",
                    "%d.%m.%Y %H:%M"
                )
            except (KeyError, TypeError, ValueError):
                continue

            if start >= now:
                upcoming.append((start, appointment))

        if not upcoming:
            return None, None

        start, appointment = min(
            upcoming,
            key=lambda item: item[0]
        )

        return {
            "start": start,
            "data": appointment,
            "services": appointment.get("services", [])
        }, None

    # SERVICES

    def show_services(self):
        self._page_heading(
            "Katalog usług",
            "Poznaj ceny i przewidywany czas zabiegów."
        )

        for service in SERVICES:
            card = self._card(
                self.page_container,
                padding=17
            )
            card.pack(fill="x", pady=5)

            row = tk.Frame(card, bg=WHITE)
            row.pack(fill="x")

            tk.Label(
                row,
                text=service["name"],
                font=("Arial", 13, "bold"),
                bg=WHITE,
                fg=TEXT,
            ).pack(side="left")

            tk.Label(
                row,
                text=(
                    f"{service['price']} PLN  ·  "
                    f"{service['duration']} min"
                ),
                font=("Arial", 11),
                bg=WHITE,
                fg=MUTED,
            ).pack(side="right")

    # CALCULATOR

    def show_calculator(self):
        open_calculator(self.page_container)

    # APPOINTMENT PLANNER

    def show_planner(self):
        AppointmentPlanner(
            self.page_container,
            on_saved=self._on_appointment_saved,
        )

    def _on_appointment_saved(self, appointment):
        self.flash_message = (
            f"Wizyta zapisana: "
            f"{appointment['date']} o {appointment['time']}."
        )

        self.show_page("home")

    # BEAUTY GUIDE

    def show_guide(self):
        self._page_heading(
            "Poradnik pielęgnacyjny",
            "Kilka prostych wskazówek przed wizytą w salonie."
        )

        tips = (
            (
                "Przed zabiegiem",
                "Przyjdź kilka minut wcześniej i poinformuj kosmetologa o alergiach."
            ),
            (
                "Pielęgnacja skóry",
                "Stosuj delikatne kosmetyki i pamiętaj o codziennej ochronie SPF."
            ),
            (
                "Po wizycie",
                "Przestrzegaj zaleceń specjalisty i unikaj drażniących produktów."
            ),
        )

        for title, description in tips:
            card = self._card(
                self.page_container
            )
            card.pack(fill="x", pady=6)

            tk.Label(
                card,
                text=title,
                font=("Arial", 13, "bold"),
                bg=WHITE,
                fg=TEXT,
            ).pack(anchor="w")

            tk.Label(
                card,
                text=description,
                font=("Arial", 10),
                bg=WHITE,
                fg=MUTED,
                wraplength=720,
                justify="left",
            ).pack(anchor="w", pady=(5, 0))

    # ABOUT SALON

    def show_about(self):
        self._page_heading(
            "O salonie",
            "URODY — miejsce na chwilę relaksu i pielęgnacji."
        )

        card = self._card(
            self.page_container,
            padding=22
        )
        card.pack(fill="x")

        tk.Label(
            card,
            text="Godziny otwarcia",
            font=("Arial", 14, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Poniedziałek–piątek, 09:00–18:00",
            font=("Arial", 11),
            bg=WHITE,
            fg=MUTED,
        ).pack(anchor="w", pady=(5, 15))

        tk.Label(
            card,
            text=(
                "Zapraszamy na manicure, pedicure, "
                "zabiegi pielęgnacyjne i stylizację brwi."
            ),
            font=("Arial", 10),
            bg=WHITE,
            fg=MUTED,
            wraplength=700,
            justify="left",
        ).pack(anchor="w")


# START APPLICATION

def main():
    root = tk.Tk()
    UrodyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
