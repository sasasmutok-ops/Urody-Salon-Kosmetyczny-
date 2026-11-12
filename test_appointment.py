
from services import SERVICES

from modules.appointment_logic import (
    calculate_total,
    calculate_duration,
    create_appointment,
    save_appointment
)

# Select two services
selected_services = [
    SERVICES[0],
    SERVICES[1]
]

# Calculate price
total = calculate_total(selected_services)

# Calculate duration
duration = calculate_duration(selected_services)

print("Total price:", total, "PLN")
print("Total duration:", duration, "minutes")

# Create appointment
appointment = create_appointment(
    selected_services,
    "20.11.2026",
    "14:00"
)

print("Appointment:", appointment)
if appointment:
    save_appointment(appointment)
    print("Appointment saved successfully!")
