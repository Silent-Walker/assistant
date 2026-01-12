from datetime import datetime, timedelta
from app.ml.predictor import predict_skip_probability

PREFERRED_WINDOWS = {
    "PhD": ["10:00", "11:00", "16:00"],
    "App": ["14:00", "18:00", "20:00"],
    "Personal": ["07:00", "21:00"],
    "General": ["12:00", "15:00"]
}


def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def find_better_time(category, used_times):
    for t in PREFERRED_WINDOWS.get(category, []):
        if t not in used_times:
            return t
    return None


def auto_reschedule(task):
    """
    Decides whether to reschedule a task.
    """
    hour = int(task["time"].split(":")[0])
    day_of_week = datetime.now().weekday()

    category_vector = {}  # built from training schema
    skip_prob = predict_skip_probability(hour, day_of_week, category_vector)

    task["skip_probability"] = round(skip_prob, 2)

    if skip_prob < 0.7:
        return task, "kept"

    new_time = find_better_time(
        task.get("category", "General"),
        used_times=[]
    )

    if new_time:
        old_time = task["time"]
        task["time"] = new_time
        return task, f"rescheduled from {old_time} to {new_time}"

    return task, "kept"
