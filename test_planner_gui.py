
import tkinter as tk

from modules.appointment_planner import AppointmentPlanner


root = tk.Tk()
root.title("Urody - Planer wizyty")
root.geometry("500x600")

planner = AppointmentPlanner(root)

root.mainloop()
