"""Feature 1 — add an assignment. Owned by Henry; do not edit db.py from
here — if the interface needs to change, that's a conversation, not a
one-line fix."""

from datetime import date

import streamlit as st

from db import PRIORITIES, create_task, init_db

st.set_page_config(page_title="Add Assignment", page_icon="+", layout="centered")
init_db()

st.title("Add an Assignment")
st.caption("Log something due, across any of your courses.")

with st.form("add_assignment_form", clear_on_submit=True):
    title = st.text_input("Assignment title", placeholder="e.g. Midterm Study Guide")
    course = st.text_input("Course", placeholder="e.g. CMPE 165")
    due_date = st.date_input("Due date", value=date.today())
    est_hours = st.number_input("Estimated hours", min_value=0.0, step=0.5, value=1.0)
    priority = st.selectbox("Priority", PRIORITIES, index=1)
    submitted = st.form_submit_button("Add assignment")

if submitted:
    if not title.strip() or not course.strip():
        st.error("Title and course are both required.")
    else:
        task_id = create_task(
            title=title.strip(),
            course=course.strip(),
            due_date=due_date.strftime("%Y-%m-%d"),
            est_hours=est_hours,
            priority=priority,
        )
        st.success(
            f"Added '{title.strip()}' (id {task_id}), due {due_date.strftime('%Y-%m-%d')}. "
            "Check My Planner to see it."
        )
