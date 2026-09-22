"""Creates the tasks table and inserts sample assignments across three
courses. Three of them share a due date on purpose, so the workload
collision the app is built to surface is visible immediately."""

from db import create_task, init_db

SAMPLE_TASKS = [
    # title,                          course,      due_date,     est_hours, priority
    ("Quiz 4 Prep",                   "CMPE 172",  "2026-09-26", 1,         "Medium"),
    ("Homework 3",                    "CMPE 165",  "2026-09-28", 2,         "Medium"),
    ("Reading Reflection",            "CMPE 131",  "2026-09-30", 1,         "Low"),
    ("Midterm Study Guide",           "CMPE 165",  "2026-10-05", 4,         "High"),
    ("Lab Report 2",                  "CMPE 131",  "2026-10-05", 3,         "High"),
    ("Project Proposal",              "CMPE 172",  "2026-10-05", 5,         "High"),
    ("Group Presentation Slides",     "CMPE 165",  "2026-10-12", 3,         "Medium"),
    ("Final Project Milestone 1",     "CMPE 131",  "2026-10-15", 6,         "High"),
]


def seed() -> None:
    init_db()
    for title, course, due_date, est_hours, priority in SAMPLE_TASKS:
        create_task(title, course, due_date, est_hours, priority)
    print(f"Seeded {len(SAMPLE_TASKS)} assignments into planner.db")


if __name__ == "__main__":
    seed()
