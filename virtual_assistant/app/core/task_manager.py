from datetime import date
from app.core.routine import get_default_tasks
from app.db.database import fetch_tasks_by_date
from app.core.auto_rescheduler import auto_reschedule
from app.ml.data_logger import get_today_completed_tasks


def get_today_tasks():
    """
    Returns tasks for today.
    Priority:
    1. User-added tasks
    2. Default routine
    
    *Filters out tasks that are already logged as done/skipped/delayed*
    """
    today = date.today().isoformat()

    # 1. Fetch Candidates (DB or Default)
    tasks = fetch_tasks_by_date(today)
    
    if not tasks:
        print("[TaskManager] No user tasks found. Loading default routine.")
        tasks = get_default_tasks()
    else:
        print("[TaskManager] Loaded user tasks")

    # 2. Get list of tasks already done today
    completed_set = get_today_completed_tasks()

    final_tasks = []

    # 3. Process and Filter
    for task in tasks:
        # Apply AI rescheduling
        updated_task, action = auto_reschedule(task)
        
        # Check if this task (Title + Time) is already in the logs
        if (updated_task['title'], updated_task['time']) not in completed_set:
            print(f"[AutoScheduler] {task['title']} -> {action}")
            final_tasks.append(updated_task)
        else:
            print(f"[TaskManager] Hiding completed task: {updated_task['title']}")

    return final_tasks