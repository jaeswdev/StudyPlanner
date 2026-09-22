"""Filter assignments and mark completed work."""

from datetime import datetime
from html import escape

import streamlit as st

from db import STATUSES, init_db, list_tasks, update_status
from ui import apply_elemental_theme, page_intro, show_task_companions

DONE = STATUSES[-1]
COLLISION_COURSES = 3

st.set_page_config(page_title="My Planner", page_icon="SP", layout="centered")
init_db()
apply_elemental_theme()
page_intro("Quest log", "My Planner", "Track the path ahead and prepare for difficult weeks.")
st.markdown('<a class="scroll-top" href="#planner-top" aria-label="Scroll to top">↑<span>TOP</span></a>', unsafe_allow_html=True)

all_tasks = list_tasks()
if not all_tasks:
    st.info("Nothing here yet - add an assignment to begin your path.")
    st.stop()

complete_count = sum(task["status"] == DONE for task in all_tasks)
incomplete_count = len(all_tasks) - complete_count
show_task_companions(incomplete_count, complete_count)

progress = complete_count / len(all_tasks)
st.markdown(
    f'''<div class="progress-card">
        <div class="progress-label"><span>Quest progress</span><strong>{complete_count}/{len(all_tasks)} complete</strong></div>
        <div class="progress-track"><div class="progress-fill" style="width:{progress * 100:.1f}%"></div></div>
    </div>''',
    unsafe_allow_html=True,
)


def week_key(due_date: str) -> str:
    year, week, _ = datetime.strptime(due_date, "%Y-%m-%d").date().isocalendar()
    return f"{year}-W{week}"


week_courses: dict[str, set] = {}
for task in all_tasks:
    if task["status"] != DONE:
        week_courses.setdefault(week_key(task["due_date"]), set()).add(task["course"])
collision_weeks = {week for week, courses in week_courses.items() if len(courses) >= COLLISION_COURSES}

st.markdown("### Choose your focus")
courses = sorted({task["course"] for task in all_tasks})
course_column, status_column = st.columns(2)
with course_column:
    course_filter = st.selectbox("Course", ["All"] + courses)
with status_column:
    status_filter = st.selectbox("Status", ["All"] + list(STATUSES))

tasks = list_tasks(
    course=None if course_filter == "All" else course_filter,
    status=None if status_filter == "All" else status_filter,
)
st.markdown("### Active quests")
if not tasks:
    st.info("No assignments match that focus.")

for task in tasks:
    week = week_key(task["due_date"])
    collision = task["status"] != DONE and week in collision_weeks

    with st.container(border=True):
        details, actions = st.columns([3, 1])
        with details:
            st.markdown(
                f'<div class="quest-title">{escape(task["title"])}</div>'
                f'<span class="course-chip">{escape(task["course"])}</span>'
                f'<div class="quest-meta">Due {escape(task["due_date"])} - '
                f'{task["est_hours"]}h - {escape(task["priority"])} priority</div>',
                unsafe_allow_html=True,
            )
            if collision:
                clash = ", ".join(sorted(week_courses[week]))
                st.markdown('<span class="collision-badge">BUSY WEEK</span>', unsafe_allow_html=True)
                st.caption(f"{len(week_courses[week])} courses have work due: {clash}")
        with actions:
            status_class = task["status"].lower().replace(" ", "-")
            st.markdown(
                f'<div class="status-label">STATUS</div><span class="status-badge status-{status_class}">{escape(task["status"])}</span>',
                unsafe_allow_html=True,
            )
            selected_status = st.selectbox(
                "Quest status",
                STATUSES,
                index=list(STATUSES).index(task["status"]),
                key=f"status_{task['id']}",
                label_visibility="collapsed",
            )
            if selected_status != task["status"]:
                try:
                    update_status(task["id"], selected_status)
                except (ValueError, TypeError) as error:
                    st.error(f"Could not update status: {error}")
                else:
                    st.rerun()
