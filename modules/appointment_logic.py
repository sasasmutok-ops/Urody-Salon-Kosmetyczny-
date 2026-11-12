
from datetime import datetime, date
import json
import os


def calculate_total(selected_services):
    """Calculate total price of selected services."""
    return sum(service["price"] for service in selected_services)


def calculate_duration(selected_services):
    """Calculate total duration of selected services."""
    return sum(service["duration"] for service in selected_services)


def validate_date(selected_date):
    """Check whether appointment date is valid."""
    try:
        appointment_date = datetime.strptime(
            selected_date, "%d.%m.%Y"
        ).date()

        return appointment_date >= date.today()

    except ValueError:
        return False


def validate_time(selected_time):
    """Check whether appointment time is valid."""
    try:
        datetime.strptime(selected_time, "%H:%M")
        return True

    except ValueError:
        return False


def create_appointment(selected_services, selected_date, selected_time):
    """Create appointment information."""

    if not selected_services:
        return None

    if not validate_date(selected_date):
        return None

    if not validate_time(selected_time):
        return None

    return {
        "services": selected_services,
        "date": selected_date,
        "time": selected_time,
        "total_price": calculate_total(selected_services),
        "total_duration": calculate_duration(selected_services)
    }


def save_appointment(appointment):
    """Save appointment to a local JSON file."""

    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "appointments.json"
    )

    appointments = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            appointments = json.load(file)

    appointments.append(appointment)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            appointments,
            file,
            indent=4,
            ensure_ascii=False
        )
