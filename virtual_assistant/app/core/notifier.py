from app.core.shared import notification_queue
from app.ml.data_logger import log_event

def notify(task_name, planned_time=None, category="General"):
    message = f"Sir, it is time to {task_name}"
    print(f"[Notifier] Queued message: {message}")

    # Add to queue for the phone to pick up
    notification_queue.append(message)

    # Log event (User will confirm via UI later)
    # response_type is pending until user clicks feedback
    pass