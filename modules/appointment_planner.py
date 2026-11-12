
import tkinter as tk
from tkinter import ttk, messagebox

from services import SERVICES

from modules.appointment_logic import (
    create_appointment,
    save_appointment
)


class AppointmentPlanner:

    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(parent, padding=20)
        self.frame.pack(fill="both", expand=True)

        self.service_vars = []

        self.create_widgets()

    def create_widgets(self):

        title = ttk.Label(
            self.frame,
            text="Planer wizyty",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        ttk.Label(
            self.frame,
            text="Wybierz usługi:"
        ).pack(anchor="w")

        # Service selection
        for service in SERVICES:
            var = tk.BooleanVar()

            checkbox = ttk.Checkbutton(
                self.frame,
                text=f"{service['name']} - "
                     f"{service['price']} PLN - "
                     f"{service['duration']} min",
                variable=var
            )

            checkbox.pack(anchor="w", pady=5)

            self.service_vars.append((var, service))

        # Date selection
        ttk.Label(
            self.frame,
            text="Data wizyty (DD.MM.RRRR):"
        ).pack(anchor="w", pady=(15, 5))

        self.date_entry = ttk.Entry(self.frame)
        self.date_entry.pack(fill="x")

        # Time selection
        ttk.Label(
            self.frame,
            text="Godzina wizyty:"
        ).pack(anchor="w", pady=(15, 5))

        self.time_box = ttk.Combobox(
            self.frame,
            values=[
                "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00",
                "15:00", "16:00", "17:00"
            ],
            state="readonly"
        )

        self.time_box.pack(fill="x")

        # Summary button
        ttk.Button(
            self.frame,
            text="Podsumowanie wizyty",
            command=self.show_summary
        ).pack(pady=(20, 5))

        # Save button
        ttk.Button(
            self.frame,
            text="Zapisz wizytę",
            command=self.save_current_appointment
        ).pack(pady=5)

    def get_current_appointment(self):
        """Get and validate appointment data."""

        selected_services = [
            service
            for var, service in self.service_vars
            if var.get()
        ]

        return create_appointment(
            selected_services,
            self.date_entry.get().strip(),
            self.time_box.get().strip()
        )

    def show_summary(self):
        """Display appointment summary."""

        appointment = self.get_current_appointment()

        if appointment is None:
            messagebox.showerror(
                "Błąd",
                "Wybierz usługi, poprawną datę i godzinę."
            )
            return

        service_names = "\n".join(
            f"{service['name']} - {service['price']} PLN "
            f"({service['duration']} min)"
            for service in appointment["services"]
        )

        messagebox.showinfo(
            "Podsumowanie wizyty",
            f"Wybrane usługi:\n{service_names}\n\n"
            f"Data: {appointment['date']}\n"
            f"Godzina: {appointment['time']}\n"
            f"Cena: {appointment['total_price']} PLN\n"
            f"Czas: {appointment['total_duration']} min"
        )

    def save_current_appointment(self):
        """Save appointment to JSON file."""

        appointment = self.get_current_appointment()

        if appointment is None:
            messagebox.showerror(
                "Błąd",
                "Wybierz usługi, poprawną datę i godzinę."
            )
            return

        try:
            save_appointment(appointment)

            messagebox.showinfo(
                "Sukces",
                "Wizyta została zapisana!"
            )

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Błąd zapisu",
                str(error)
            )
