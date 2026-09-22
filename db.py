"""
Study Planner — database interface.

Frozen by Henry + Anahi. This is the one file both features depend on —
changing a signature here requires both of us to agree, out loud, first.

due_date is ALWAYS the string "YYYY-MM-DD". SQLite has no date type; it
stores whatever text you give it, so a mismatched format sorts silently
wrong instead of throwing an error. Convert at the edges:
    writing:  d.strftime("%Y-%m-%d")
    reading:  datetime.strptime(s, "%Y-%m-%d").date()
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "planner.db"

PRIORITIES = ("Low", "Medium", "High")
STATUSES = ("Not Started", "In Progress", "Done")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            course TEXT NOT NULL,
            due_date TEXT NOT NULL,
            est_hours REAL NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Not Started',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def create_task(title: str, course: str, due_date: str, est_hours: float, priority: str) -> int:
    if priority not in PRIORITIES:
        raise ValueError(f"priority must be one of {PRIORITIES}, got {priority!r}")

    conn = _connect()
    cur = conn.execute(
        """
        INSERT INTO tasks (title, course, due_date, est_hours, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, course, due_date, est_hours, priority, "Not Started", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return task_id


def list_tasks(course: str | None = None, status: str | None = None) -> list[dict]:
    conn = _connect()
    query = "SELECT * FROM tasks"
    conditions = []
    params: list[str] = []
    if course:
        conditions.append("course = ?")
        params.append(course)
    if status:
        conditions.append("status = ?")
        params.append(status)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY due_date ASC"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task(task_id: int) -> dict | None:
    conn = _connect()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_status(task_id: int, status: str) -> None:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, got {status!r}")

    conn = _connect()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
