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

# Anchored to next Monday, not today, so the collision week below always lands
# inside one Mon–Sun week whatever day you seed on. Every date is in the future.
NEXT_MONDAY = TODAY + timedelta(days=7 - TODAY.weekday())


def due_in(days):
    """A 'YYYY-MM-DD' string for N days after next Monday, so the data never goes stale."""
    return (NEXT_MONDAY + timedelta(days=days)).isoformat()


# (title, course, days after next Monday, estimated hours, priority)
#
# Wed, Wed and Thu of next week are deliberate: 17 hours of work landing in
# one week across three courses. That collision is the whole product idea,
# and it is what the Loom demo should show. The week after has only two
# courses, so it must NOT be flagged.
SAMPLE = [
    ("Reading response 4",     "CMPE 165",  0,  1.5, "Low"),
    ("Project 1 report",       "CMPE 165",  2,  8.0, "High"),     # ← collision
    ("Lab 5 — paging",         "CS 149",    2,  5.0, "High"),     # ← collision
    ("Midterm study guide",    "CS 157A",   3,  4.0, "Medium"),   # ← collision
    ("Quiz 6",                 "CMPE 165",  8,  1.0, "Medium"),
    ("Homework 3",             "CS 149",   10,  3.0, "Medium"),
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