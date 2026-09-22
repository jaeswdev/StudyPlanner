"""
Study Planner — home page.

Streamlit turns every file in the pages/ folder into its own tab in the
left sidebar, automatically. This file is only the landing page: it says
what the app is. The two features live in pages/ and are owned by one
person each, which is why neither of us ever edits this file after today.

Run with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Study Planner",
    page_icon="📚",
    layout="centered",
)

st.title("Study Planner")
st.caption("CMPE 165 · Henry Lee & Anahi Carrasco")

st.markdown(
    """
    A course-load planner for students taking several classes at once.

    A calendar tells you **when** something is due. It cannot tell you that
    three of your courses have major deliverables in the same week — and that
    collision is what turns into a late withdrawal.

    **Use the sidebar:**

    - **Add Assignment** — record an assignment with its course and due date
    - **My Planner** — everything sorted by due date, filterable, markable as done
    """
)

st.divider()
st.success("Environment check passed — if you can read this in a browser, you're set up.")