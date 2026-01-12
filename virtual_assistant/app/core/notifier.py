import pyttsx3
from app.ml.data_logger import log_event

engine = pyttsx3.init()

def notify(task_name, planned_time=None, category="General"):
    message = f"Sir, it is time to {task_name}"
    print(f"[Notifier] {message}")

    engine.say(message)
    engine.runAndWait()

    # TEMP behavior assumption
    # (Later replaced by mobile feedback)
    response_type = "ignored"

    log_event(
        task=task_name,
        planned_time=planned_time,
        response_type=response_type,
        category=category
    )
