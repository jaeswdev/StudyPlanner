"""Feature 1 — add an assignment. Owned by Henry; do not edit db.py from
here — if the interface needs to change, that's a conversation, not a
one-line fix."""

from datetime import date

import streamlit as st

from db import PRIORITIES, create_task, init_db
from ui import apply_elemental_theme, page_intro

st.set_page_config(page_title="Add Assignment", page_icon="SP", layout="centered")
init_db()
apply_elemental_theme()
page_intro("Quest board", "Add an Assignment", "Start a new quest by giving each task a clear place in your semester.")

# Success message survives the rerun below (it's set the run before this one).
if "add_assignment_success" in st.session_state:
    st.success(st.session_state.pop("add_assignment_success"))

# Widget keys are suffixed with this counter so we can reset the form to
# blank after a real success — without clear_on_submit, which wipes
# everything you typed even when Enter fires the submit on a half-filled
# form and validation rejects it.
if "add_assignment_form_version" not in st.session_state:
    st.session_state.add_assignment_form_version = 0
version = st.session_state.add_assignment_form_version

with st.form("add_assignment_form", clear_on_submit=False):
    title = st.text_input(
        "Assignment title", placeholder="e.g. Midterm Study Guide", key=f"title_{version}"
    )
    course = st.text_input("Course", placeholder="e.g. CMPE 165", key=f"course_{version}")
    due_date = st.date_input("Due date", value=date.today(), key=f"due_date_{version}")
    est_hours = st.number_input(
        "Estimated hours", min_value=0.0, step=0.5, value=1.0, key=f"est_hours_{version}"
    )
    priority = st.selectbox("Priority", PRIORITIES, index=1, key=f"priority_{version}")
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
        st.session_state.add_assignment_success = (
            f"Added '{title.strip()}' (id {task_id}), due {due_date.strftime('%Y-%m-%d')}. "
            "Check My Planner to see it."
        )
        st.session_state.add_assignment_form_version += 1
        st.rerun()
