import datetime
import os

def log_alert(message):
    os.makedirs("logs", exist_ok=True)

    with open("logs/alerts.log", "a") as file:
        time = datetime.datetime.now()
        file.write(f"[{time}] {message}\n")