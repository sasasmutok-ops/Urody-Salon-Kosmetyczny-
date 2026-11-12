
import tkinter as tk
from services import SERVICES


class PriceCalculator:

    def __init__(self, parent):
        self.parent = parent
        self.selected_services = []

    def open(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Kalkulator cen - URODY")
        self.window.geometry("500x550")
        self.window.minsize(400, 450)
        self.window.configure(bg="#FFF5F7")

        self.create_header()
        self.create_services()
        self.create_total()
        self.create_clear_button()

    def create_header(self):
        tk.Label(
            self.window,
            text="KALKULATOR CEN",
            font=("Arial", 22, "bold"),
            bg="#FFF5F7",
            fg="#713B50"
        ).pack(pady=(25, 10))

        tk.Label(
            self.window,
            text="Wybierz interesujące Cię usługi:",
            font=("Arial", 12),
            bg="#FFF5F7",
            fg="#555555"
        ).pack(pady=10)

    def create_services(self):
        frame = tk.Frame(
            self.window,
            bg="#FFF5F7"
        )
        frame.pack(fill="both", padx=30, pady=10)

        for service in SERVICES:
            variable = tk.BooleanVar(value=False)

            self.selected_services.append(
                (service, variable)
            )

            service_frame = tk.Frame(
                frame,
                bg="white",
                padx=15,
                pady=12
            )
            service_frame.pack(fill="x", pady=5)

            tk.Checkbutton(
                service_frame,
                text=service["name"],
                variable=variable,
                command=self.update_total,
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#713B50",
                activebackground="white",
                selectcolor="#FFF5F7"
            ).pack(side="left")

            tk.Label(
                service_frame,
                text=f'{service["price"]} PLN',
                font=("Arial", 11),
                bg="white",
                fg="#555555"
            ).pack(side="right")

    def create_total(self):
        self.total_label = tk.Label(
            self.window,
            text="Łączna cena: 0 PLN",
            font=("Arial", 20, "bold"),
            bg="#FFF5F7",
            fg="#D98CA5"
        )
        self.total_label.pack(pady=25)

    def update_total(self):
        total = sum(
            service["price"]
            for service, variable in self.selected_services
            if variable.get()
        )

        self.total_label.config(
            text=f"Łączna cena: {total} PLN"
        )

    def create_clear_button(self):
        tk.Button(
            self.window,
            text="Wyczyść wybór",
            command=self.clear_selection,
            font=("Arial", 11, "bold"),
            bg="#D98CA5",
            fg="white",
            activebackground="#C47791",
            relief="flat",
            cursor="hand2",
            width=20,
            height=2
        ).pack(pady=10)

    def clear_selection(self):
        for service, variable in self.selected_services:
            variable.set(False)

        self.update_total()


def open_calculator(parent):
    calculator = PriceCalculator(parent)
    calculator.open()
