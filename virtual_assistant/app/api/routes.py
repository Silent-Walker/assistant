from fastapi import APIRouter
from datetime import date
from app.db.database import add_task, fetch_tasks_by_date
from app.core.scheduler import schedule_tasks
from app.core.task_manager import get_today_tasks
from app.ml.data_logger import log_event
from datetime import datetime

router = APIRouter()


@router.post("/add-task")
def add_new_task(time: str, title: str):
    today = date.today().isoformat()
    add_task(today, time, title)

    tasks = get_today_tasks()
    schedule_tasks(tasks)

    return {"status": "Task added and scheduled"}


@router.get("/today-tasks")
def get_today():
    today = date.today().isoformat()
    return fetch_tasks_by_date(today)

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