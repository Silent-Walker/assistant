import csv
import os
from datetime import datetime

LOG_FILE = "data/user_logs.csv"
HEADERS = [
    "date",
    "task",
    "planned_time",
    "actual_response_time",
    "response_type",
    "category"
]

def init_logger():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def log_event(task, planned_time, response_type, category="General"):
    now = datetime.now()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            now.date(),
            task,
            planned_time,
            now.strftime("%H:%M"),
            response_type,
            category
        ])
