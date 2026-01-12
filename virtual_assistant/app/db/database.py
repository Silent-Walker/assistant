import sqlite3

DB_PATH = "data/tasks.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            date TEXT,
            time TEXT,
            title TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_task(task_date, time, title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks VALUES (?, ?, ?)",
        (task_date, time, title)
    )
    conn.commit()
    conn.close()


def fetch_tasks_by_date(task_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT time, title FROM tasks WHERE date = ?",
        (task_date,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"time": r[0], "title": r[1]} for r in rows]
