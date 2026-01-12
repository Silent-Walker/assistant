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
    
    # Ensure file exists
    if not os.path.exists(LOG_FILE):
        init_logger()

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

def get_today_completed_tasks():
    """
    Returns a set of (title, time) tuples for tasks completed today.
    """
    if not os.path.exists(LOG_FILE):
        return set()

    completed = set()
    today_str = datetime.now().date().isoformat()

    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if the log entry is for today
                if row['date'] == today_str:
                    completed.add((row['task'], row['planned_time']))
    except Exception as e:
        print(f"[DataLogger] Error reading logs: {e}")

    return completed