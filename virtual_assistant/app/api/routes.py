from fastapi import APIRouter, HTTPException
from datetime import date, datetime
from app.db.database import add_task, fetch_tasks_by_date
from app.core.scheduler import schedule_tasks
from app.core.task_manager import get_today_tasks
from app.ml.data_logger import log_event

router = APIRouter()

@router.post("/add-task")
def add_new_task(time: str, title: str, category: str = "General"):
    today = date.today().isoformat()
    
    # --- SMART FEATURE: CONFLICT DETECTION ---
    current_tasks = fetch_tasks_by_date(today)
    for t in current_tasks:
        if t['time'] == time:
            raise HTTPException(
                status_code=400, 
                detail=f"Conflict! You already have '{t['title']}' scheduled at {time}."
            )
    # -----------------------------------------

    # Add to DB (Note: You might want to update add_task DB signature later to store category permanently)
    add_task(today, time, title)

    # Reload and reschedule
    tasks = get_today_tasks()
    schedule_tasks(tasks)

    return {"status": "Task added and scheduled"}


@router.get("/today-tasks")
def get_today():
    # This now uses the smart task manager which mixes default routine + user tasks
    return get_today_tasks()

@router.post("/task-feedback")
def task_feedback(
    task: str,
    planned_time: str,
    response_type: str,  # done / delayed / skipped
    category: str = "General"
):
    log_event(
        task=task,
        planned_time=planned_time,
        response_type=response_type,
        category=category
    )

    return {
        "status": "Feedback recorded",
        "time": datetime.now().strftime("%H:%M")
    }