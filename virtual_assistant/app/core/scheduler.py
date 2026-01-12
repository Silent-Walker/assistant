from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.core.notifier import notify

scheduler = BackgroundScheduler()


def schedule_tasks(tasks):
    scheduler.remove_all_jobs()

    for task in tasks:
        hour, minute = map(int, task["time"].split(":"))

        run_time = datetime.now().replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if run_time < datetime.now():
            continue

        scheduler.add_job(
            notify,
            'date',
            run_date=run_time,
            args=[task["title"], task["time"]],
            id=f"{task['title']}_{task['time']}"
        )

        print(f"[Scheduler] Scheduled {task['title']} at {task['time']}")
