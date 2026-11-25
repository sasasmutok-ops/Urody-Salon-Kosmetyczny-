
"""Modern inline price calculator for Urody."""

import tkinter as tk

from services import SERVICES


# Modern Urody color palette
BG = "#F5F5F0"
GREEN = "#34483D"
GREEN_DARK = "#26372F"
TEXT = "#26332C"
MUTED = "#747B73"
WHITE = "#FFFFFF"
BORDER = "#E1E5DD"
SAGE = "#E9EEE8"
GOLD = "#B49A70"


class PriceCalculator:

    def __init__(self, parent):
        self.parent = parent
        self.selected_services = []

        self.view = tk.Frame(parent, bg=BG)
        self.view.pack(fill="both", expand=True)

        self.create_content()

    def create_content(self):

        # Page heading
        tk.Label(
            self.view,
            text="Kalkulator cen",
            font=("Arial", 24, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            self.view,
            text="Wybierz zabiegi i sprawdź łączny koszt.",
            font=("Arial", 11),
            bg=BG,
            fg=MUTED,
        ).pack(anchor="w", pady=(0, 22))

        # Services card
        card = tk.Frame(
            self.view,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=16,
        )
        card.pack(fill="x", pady=(0, 18))

        tk.Label(
            card,
            text="Dostępne zabiegi",
            font=("Arial", 14, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 12))

        for index, service in enumerate(SERVICES):

            row = tk.Frame(
                card,
                bg=WHITE,
                pady=9,
            )
            row.pack(fill="x")

            variable = tk.BooleanVar(value=False)

            self.selected_services.append(
                (service, variable)
            )

            # Checkbutton with readable colors
            check = tk.Checkbutton(
                row,
                text=service["name"],
                variable=variable,
                command=self.update_total,
                font=("Arial", 12, "bold"),
                bg=WHITE,
                fg=TEXT,
                activebackground=WHITE,
                activeforeground=GREEN,
                selectcolor=SAGE,
                bd=0,
                highlightthickness=0,
                cursor="hand2",
            )
            check.pack(side="left")

            tk.Label(
                row,
                text=f"{service['duration']} min",
                font=("Arial", 10),
                bg=WHITE,
                fg=MUTED,
            ).pack(side="left", padx=(12, 0))

            tk.Label(
                row,
                text=f"{service['price']} PLN",
                font=("Arial", 12, "bold"),
                bg=WHITE,
                fg=GREEN,
            ).pack(side="right")

            if index < len(SERVICES) - 1:
                tk.Frame(
                    card,
                    bg=BORDER,
                    height=1,
                ).pack(fill="x")

        # Total card
        total_card = tk.Frame(
            self.view,
            bg=GREEN,
            padx=22,
            pady=20,
        )
        total_card.pack(fill="x", pady=(0, 16))

        tk.Label(
            total_card,
            text="ŁĄCZNY KOSZT",
            font=("Arial", 10, "bold"),
            bg=GREEN,
            fg="#DCE5DC",
        ).pack(anchor="w")

        self.total_label = tk.Label(
            total_card,
            text="0 PLN",
            font=("Arial", 27, "bold"),
            bg=GREEN,
            fg=WHITE,
        )
        self.total_label.pack(anchor="w", pady=(5, 0))

        self.count_label = tk.Label(
            total_card,
            text="Nie wybrano żadnych usług",
            font=("Arial", 10),
            bg=GREEN,
            fg="#DCE5DC",
        )
        self.count_label.pack(anchor="w", pady=(4, 0))

        # Buttons
        buttons = tk.Frame(
            self.view,
            bg=BG,
        )
        buttons.pack(anchor="w")

        self.clear_button = tk.Button(
            buttons,
            text="Wyczyść wybór",
            command=self.clear_selection,
            font=("Arial", 10, "bold"),
            bg=SAGE,
            fg=GREEN,
            activebackground="#DCE5DC",
            activeforeground=GREEN_DARK,
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
        )
        self.clear_button.pack(side="left")

    def update_total(self):

        selected = [
            service
            for service, variable in self.selected_services
            if variable.get()
        ]

        total = sum(
            service["price"]
            for service in selected
        )

        count = len(selected)

        self.total_label.configure(
            text=f"{total} PLN"
        )

        if count == 0:
            self.count_label.configure(
                text="Nie wybrano żadnych usług"
            )
        elif count == 1:
            self.count_label.configure(
                text="Wybrano 1 usługę"
            )
        else:
            self.count_label.configure(
                text=f"Wybrano {count} usługi"
            )

    def clear_selection(self):

        for _service, variable in self.selected_services:
            variable.set(False)

        self.update_total()


def open_calculator(parent):
    """Render the calculator inside the supplied page container."""
    return PriceCalculator(parent)
