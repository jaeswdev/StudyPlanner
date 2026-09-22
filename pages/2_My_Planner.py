"""Feature 2 — my planner: filter and mark done. Owned by Anahi; do not
edit db.py from here."""

from datetime import datetime

import streamlit as st

from db import STATUSES, init_db, list_tasks, update_status

st.set_page_config(page_title="My Planner", page_icon="📋", layout="centered")
init_db()

st.title("My Planner")
st.caption("Everything due, sorted by date. Filter it, then mark things done.")

all_tasks = list_tasks()

if not all_tasks:
    st.info("Nothing here yet — add an assignment on the Add Assignment page.")
    st.stop()


def week_key(due_date: str) -> str:
    year, week, _ = datetime.strptime(due_date, "%Y-%m-%d").date().isocalendar()
    return f"{year}-W{week}"


# a week where 2+ courses have something due is the collision the app exists to surface
week_courses: dict[str, set] = {}
for t in all_tasks:
    week_courses.setdefault(week_key(t["due_date"]), set()).add(t["course"])
collision_weeks = {wk for wk, courses in week_courses.items() if len(courses) > 1}

courses = sorted({t["course"] for t in all_tasks})
col1, col2 = st.columns(2)
with col1:
    course_filter = st.selectbox("Course", ["All"] + courses)
with col2:
    status_filter = st.selectbox("Status", ["All"] + list(STATUSES))

tasks = list_tasks(
    course=None if course_filter == "All" else course_filter,
    status=None if status_filter == "All" else status_filter,
)

if not tasks:
    st.info("No assignments match that filter.")

for t in tasks:
    collision = week_key(t["due_date"]) in collision_weeks
    with st.container(border=True):
        left, right = st.columns([3, 1])
        with left:
            title = f"**{t['title']}** — {t['course']}"
            if collision:
                title += " ⚠️"
            st.markdown(title)
            st.caption(f"Due {t['due_date']} · {t['est_hours']}h · {t['priority']} priority")
            if collision:
                st.caption("⚠️ Another course also has something due this week.")
        with right:
            st.markdown(f"`{t['status']}`")
            if t["status"] != "Done" and st.button("Mark done", key=f"done_{t['id']}"):
                update_status(t["id"], "Done")
                st.rerun()
