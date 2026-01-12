import pyttsx3
from app.ml.data_logger import log_event

engine = pyttsx3.init()

def notify(task_name, planned_time=None, category="General"):
    message = f"Sir, it is time to {task_name}"
    print(f"[Notifier] {message}")

    try:
        engine.say(message)
        engine.runAndWait()
    except RuntimeError:
        # Handle cases where the loop is already running
        pass

    # FIX: Do NOT log "ignored" here immediately. 
    # Let the user feedback API handle the logging of the actual response.
    # This prevents creating false negative data points.