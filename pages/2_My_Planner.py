"""Feature 2 — my planner: filter and mark done. Owned by Henry; do not
edit db.py from here."""

from datetime import datetime

import streamlit as st

from db import STATUSES, init_db, list_tasks, update_status

DONE = STATUSES[-1]       # "Done", taken from db rather than retyped
COLLISION_COURSES = 3     # courses with open work in one week that count as a collision

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


# three courses with unfinished work in the same Mon–Sun week is the collision
# the app exists to surface; finished work no longer counts toward it
week_courses: dict[str, set] = {}
for t in all_tasks:
    if t["status"] != DONE:
        week_courses.setdefault(week_key(t["due_date"]), set()).add(t["course"])
collision_weeks = {wk for wk, c in week_courses.items() if len(c) >= COLLISION_COURSES}

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
    wk = week_key(t["due_date"])
    collision = t["status"] != DONE and wk in collision_weeks
    with st.container(border=True):
        left, right = st.columns([3, 1])
        with left:
            title = f"**{t['title']}** — {t['course']}"
            if collision:
                title += " ⚠️"
            st.markdown(title)
            st.caption(f"Due {t['due_date']} · {t['est_hours']}h · {t['priority']} priority")
            if collision:
                clash = ", ".join(sorted(week_courses[wk]))
                st.caption(f"⚠️ {len(week_courses[wk])} courses have work due this week: {clash}")
        with right:
            st.markdown(f"`{t['status']}`")
            if t["status"] != DONE and st.button("Mark done", key=f"done_{t['id']}"):
                try:
                    update_status(t["id"], DONE)
                except (ValueError, TypeError) as e:
                    st.error(f"Couldn't mark it done: {e}")
                else:
                    st.rerun()
