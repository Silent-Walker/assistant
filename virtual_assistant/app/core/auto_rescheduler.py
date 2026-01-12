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
    try:
        hour = int(task["time"].split(":")[0])
    except ValueError:
        # Handle cases where time might be invalid
        return task, "kept"

    day_of_week = datetime.now().weekday()

    # FIX: Manually construct one-hot encoding for the model.
    # Based on trainer.py using drop_first=True on ["App", "General", "Personal", "PhD"]
    # "App" is likely dropped as the reference category.
    current_category = task.get("category", "General")
    
    category_vector = {
        "category_General": 1 if current_category == "General" else 0,
        "category_Personal": 1 if current_category == "Personal" else 0,
        "category_PhD": 1 if current_category == "PhD" else 0
    }

    skip_prob = predict_skip_probability(hour, day_of_week, category_vector)

    task["skip_probability"] = round(skip_prob, 2)

    # Threshold for rescheduling
    if skip_prob < 0.7:
        return task, "kept"

    new_time = find_better_time(
        current_category,
        used_times=[]
    )

    if new_time:
        old_time = task["time"]
        task["time"] = new_time
        return task, f"rescheduled from {old_time} to {new_time}"

    return task, "kept"