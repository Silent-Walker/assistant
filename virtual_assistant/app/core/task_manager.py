from datetime import date
from app.core.routine import get_default_tasks
from app.db.database import fetch_tasks_by_date
from app.core.auto_rescheduler import auto_reschedule


def get_today_tasks():
    """
    Returns tasks for today.
    Priority:
    1. User-added tasks
    2. Default routine
    """
    today = date.today().isoformat()

    tasks = fetch_tasks_by_date(today) or get_default_tasks()
    final_tasks = []

    for task in tasks:
        updated_task, action = auto_reschedule(task)
        print(f"[AutoScheduler] {task['title']} → {action}")
        final_tasks.append(updated_task)

    if final_tasks:
        print("[TaskManager] Loaded user tasks")
        return final_tasks

    print("[TaskManager] No user tasks found. Loading default routine.")
    return get_default_tasks()


