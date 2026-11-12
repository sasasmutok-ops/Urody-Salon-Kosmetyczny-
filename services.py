
SERVICES = [
    {
        "name": "Manicure",
        "price": 80,
        "duration": 60
    },
    {
        "name": "Pedicure",
        "price": 120,
        "duration": 90
    },
    {
        "name": "Facial treatment",
        "price": 150,
        "duration": 60
    },
    {
        "name": "Eyebrow styling",
        "price": 50,
        "duration": 30
    }
]


def show_services():
    print("\n===== URODY - KATALOG USLUG =====")

    for service in SERVICES:
        print(
            f"{service['name']} | "
            f"{service['price']} PLN | "
            f"{service['duration']} min"
        )


if __name__ == "__main__":
    show_services()
