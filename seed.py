"""
seed.py — create the database and fill it with realistic sample data.

Run:  python3 seed.py

Deleting planner.db and re-running this is our TESTED CONTINGENCY for
Part K. It takes about a second and proves the restore path actually
works — which is exactly what GitLab never did (Lecture 6, slides 52-53).
"""

from datetime import date, timedelta

import db

TODAY = date.today()


def due_in(days):
    """A 'YYYY-MM-DD' string for N days from today, so the data never goes stale."""
    return (TODAY + timedelta(days=days)).isoformat()


# (title, course, days from today, estimated hours, priority)
#
# Days 3, 3 and 4 are deliberate: 17 hours of work landing in one week
# across three courses. That collision is the whole product idea, and it
# is what the Loom demo should show.
SAMPLE = [
    ("Reading response 4",     "CMPE 165",  2,  1.5, "Low"),
    ("Project 1 report",       "CMPE 165",  3,  8.0, "High"),     # ← collision
    ("Lab 5 — paging",         "CS 149",    3,  5.0, "High"),     # ← collision
    ("Midterm study guide",    "CS 157A",   4,  4.0, "Medium"),   # ← collision
    ("Quiz 6",                 "CMPE 165",  9,  1.0, "Medium"),
    ("Homework 3",             "CS 149",   11,  3.0, "Medium"),
    ("ER diagram draft",       "CS 157A",  14,  2.5, "Medium"),
    ("Final project proposal", "CS 157A",  21,  6.0, "High"),
]


def main():
    db.init_db()

    if db.list_tasks():
        print("Database already has data — nothing inserted.")
        print("Delete planner.db first if you want a clean reseed.")
        return

    new_ids = []
    for title, course, offset, hours, priority in SAMPLE:
        task_id = db.create_task(title, course, due_in(offset), hours, priority)
        new_ids.append(task_id)
        print(f"  [{task_id}] {due_in(offset)}  {course:9} {title}")

    # Vary the statuses so the filter has something to filter.
    db.update_status(new_ids[0], "Done")
    db.update_status(new_ids[2], "In Progress")

    print(f"\nSeeded {len(SAMPLE)} assignments.")


if __name__ == "__main__":
    main()