"""
db.py — the data layer for Study Planner.

FROZEN Mon 6:15 PM, agreed by Henry Lee and Anahi Carrasco.

Both feature pages import this module. It is the one interface we share,
so changing a signature, a dict key, or an allowed value here requires
both of us to agree out loud BEFORE the change is pushed.

PUBLIC API — five functions, nothing else
-----------------------------------------
    init_db()                                                  -> None
    create_task(title, course, due_date, est_hours, priority)   -> int
    list_tasks(course=None, status=None)                        -> list[dict]
    get_task(task_id)                                           -> dict | None
    update_status(task_id, status)                              -> None

Every task dict has EXACTLY these keys:
    id, title, course, due_date, est_hours, priority, status, created_at

Allowed values — capital letters matter:
    priority : "Low" | "Medium" | "High"
    status   : "Not Started" | "In Progress" | "Done"

due_date is ALWAYS the string "YYYY-MM-DD".
SQLite has no date type. It stores whatever you hand it as text, silently.
"YYYY-MM-DD" is the only common format that sorts correctly as text.
create_task() accepts a date object OR that string and normalises it;
everything read back out is that string.
"""

import sqlite3
from contextlib import closing
from datetime import date, datetime
from pathlib import Path

# Anchored to this file's folder so it works no matter where you run from.
DB_PATH = Path(__file__).parent / "planner.db"

PRIORITIES = ("Low", "Medium", "High")
STATUSES = ("Not Started", "In Progress", "Done")
DATE_FORMAT = "%Y-%m-%d"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      # rows become dict-able by column name
    return conn


def _normalise_date(value):
    """
    Accept a date, a datetime, or a "YYYY-MM-DD" string.
    Always return a "YYYY-MM-DD" string. Reject anything else loudly.

    This is the most important function in the file. It is the boundary
    where an ambiguous date becomes an unambiguous one.
    """
    if isinstance(value, datetime):      # must be checked BEFORE date
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip(), DATE_FORMAT).date().isoformat()
        except ValueError:
            raise ValueError(
                f"due_date must be 'YYYY-MM-DD', got {value!r}. "
                "If it came from st.date_input, pass the date object straight in."
            ) from None
    raise TypeError(
        f"due_date must be a date or a 'YYYY-MM-DD' string, "
        f"got {type(value).__name__}"
    )


def init_db():
    """Create the table if it does not exist. Safe to call on every page load."""
    with closing(_connect()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT NOT NULL,
                course     TEXT NOT NULL,
                due_date   TEXT NOT NULL,
                est_hours  REAL NOT NULL DEFAULT 1.0,
                priority   TEXT NOT NULL DEFAULT 'Medium'
                           CHECK (priority IN ('Low', 'Medium', 'High')),
                status     TEXT NOT NULL DEFAULT 'Not Started'
                           CHECK (status IN ('Not Started', 'In Progress', 'Done')),
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def create_task(title, course, due_date, est_hours, priority):
    """Insert one assignment. Returns the new row's id."""
    title = (title or "").strip()
    course = (course or "").strip()
    if not title:
        raise ValueError("title is required")
    if not course:
        raise ValueError("course is required")
    if priority not in PRIORITIES:
        raise ValueError(f"priority must be one of {PRIORITIES}, got {priority!r}")

    due_date = _normalise_date(due_date)

    with closing(_connect()) as conn, conn:
        cur = conn.execute(
            """INSERT INTO tasks (title, course, due_date, est_hours, priority, status)
               VALUES (?, ?, ?, ?, ?, 'Not Started')""",
            (title, course, due_date, float(est_hours), priority),
        )
        return cur.lastrowid


def list_tasks(course=None, status=None):
    """
    Assignments as a list of dicts.

    Sorted by due_date ascending (soonest first), then High priority
    before Medium before Low, then title. Pass course and/or status to
    filter; pass neither to get everything.
    """
    sql = "SELECT * FROM tasks"
    clauses, params = [], []
    if course:
        clauses.append("course = ?")
        params.append(course.strip())
    if status:
        clauses.append("status = ?")
        params.append(status)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += """
        ORDER BY due_date ASC,
                 CASE priority
                      WHEN 'High' THEN 0
                      WHEN 'Medium' THEN 1
                      ELSE 2
                 END,
                 title ASC
    """
    with closing(_connect()) as conn:
        return [dict(row) for row in conn.execute(sql, params)]


def get_task(task_id):
    """One assignment by id, or None if it does not exist."""
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (int(task_id),)
        ).fetchone()
        return dict(row) if row else None


def update_status(task_id, status):
    """Change one assignment's status. Raises if the id or status is wrong."""
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, got {status!r}")
    with closing(_connect()) as conn, conn:
        cur = conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (status, int(task_id))
        )
        if cur.rowcount == 0:
            raise ValueError(f"no task with id {task_id}")