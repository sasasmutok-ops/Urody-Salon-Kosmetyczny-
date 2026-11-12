
import tkinter as tk
from tkinter import messagebox

from services import SERVICES
from calculator import open_calculator


class UrodyApp:

    def __init__(self, root):
        self.root = root

        self.root.title("URODY - Salon Kosmetyczny")
        self.root.geometry("900x600")
        self.root.minsize(750, 500)
        self.root.configure(bg="#FFF5F7")

        self.create_header()
        self.create_content()

    # HEADER
    def create_header(self):
        header = tk.Frame(
            self.root,
            bg="#D98CA5",
            height=110
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="URODY",
            font=("Arial", 30, "bold"),
            bg="#D98CA5",
            fg="white"
        ).pack(pady=(15, 0))

        tk.Label(
            header,
            text="SALON KOSMETYCZNY",
            font=("Arial", 12),
            bg="#D98CA5",
            fg="white"
        ).pack()

    # MAIN CONTENT
    def create_content(self):
        content = tk.Frame(
            self.root,
            bg="#FFF5F7"
        )
        content.pack(
            expand=True,
            fill="both",
            padx=30,
            pady=25
        )

        tk.Label(
            content,
            text="Witamy w salonie Urody!",
            font=("Arial", 24, "bold"),
            bg="#FFF5F7",
            fg="#713B50"
        ).pack(pady=15)

        tk.Label(
            content,
            text="Wybierz interesującą Cię funkcję:",
            font=("Arial", 13),
            bg="#FFF5F7",
            fg="#555555"
        ).pack(pady=10)

        buttons = [
            ("Katalog usług", self.show_services),
            ("Kalkulator cen", self.show_calculator),
            ("Planer wizyty", self.show_planner),
            ("Poradnik pielęgnacyjny", self.show_guide),
            ("Informacje o salonie", self.show_about)
        ]

        for text, command in buttons:
            tk.Button(
                content,
                text=text,
                command=command,
                font=("Arial", 13, "bold"),
                bg="#D98CA5",
                fg="white",
                activebackground="#C47791",
                activeforeground="white",
                width=28,
                height=2,
                relief="flat",
                cursor="hand2"
            ).pack(pady=5)

    # SERVICES CATALOG
    def show_services(self):
        window = tk.Toplevel(self.root)

        window.title("Katalog usług - URODY")
        window.geometry("500x430")
        window.configure(bg="#FFF5F7")

        tk.Label(
            window,
            text="KATALOG USŁUG",
            font=("Arial", 22, "bold"),
            bg="#FFF5F7",
            fg="#713B50"
        ).pack(pady=20)

        for service in SERVICES:

            frame = tk.Frame(
                window,
                bg="white",
                padx=15,
                pady=10
            )
            frame.pack(
                fill="x",
                padx=25,
                pady=6
            )

            tk.Label(
                frame,
                text=service["name"],
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#713B50"
            ).pack(anchor="w")

            tk.Label(
                frame,
                text=f'Cena: {service["price"]} PLN | '
                     f'Czas: {service["duration"]} min',
                font=("Arial", 11),
                bg="white",
                fg="#555555"
            ).pack(anchor="w")

    # PRICE CALCULATOR
    def show_calculator(self):
        open_calculator(self.root)

    # APPOINTMENT PLANNER
    def show_planner(self):
        messagebox.showinfo(
            "Planer wizyty",
            "Planer wizyt będzie dostępny wkrótce."
        )

    # BEAUTY GUIDE
    def show_guide(self):
        messagebox.showinfo(
            "Poradnik pielęgnacyjny",
            "Porady pielęgnacyjne będą dostępne wkrótce."
        )

    # ABOUT SALON
    def show_about(self):
        messagebox.showinfo(
            "O salonie",
            "URODY - Salon Kosmetyczny\n\n"
            "Godziny otwarcia:\n"
            "Poniedziałek - Piątek, 9:00-18:00\n\n"
            "Zapraszamy!"
        )


# APPLICATION START
def main():
    root = tk.Tk()
    app = UrodyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
