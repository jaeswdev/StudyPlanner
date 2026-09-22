"""Study Planner landing page."""

import streamlit as st

from ui import apply_elemental_theme, page_intro

st.set_page_config(page_title="Study Planner", page_icon="SP", layout="centered")
apply_elemental_theme()

page_intro("Study quest", "Study Planner", "Plan your path across the semester.")

st.markdown(
    """
    <div class="welcome-card">
      <h2>Stay ahead of the storm.</h2>
      <p>Keep every assignment in one place, see busy weeks early, and make progress at your own pace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

plan, prepare, complete = st.columns(3)
with plan:
    st.page_link("pages/1_Add_Assignment.py", label="Plan", use_container_width=True)
with prepare:
    st.page_link("pages/2_My_Planner.py", label="Prepare", use_container_width=True)
with complete:
    st.page_link("pages/2_My_Planner.py", label="Complete", use_container_width=True)

st.markdown("### Your path")
left, right = st.columns(2)
with left:
    st.markdown("**01 - Add a quest**  \nRecord an assignment with its course, deadline, and effort.")
with right:
    st.markdown("**02 - Check your quest log**  \nReview what is due and finish tasks as you go.")

st.divider()
st.info("Tip: use My Planner to spot weeks with several courses due at once.")
