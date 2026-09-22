# Study Planner

CMPE 165 · Project 1 — Henry Lee & Anahi Carrasco

## What this is

A course-load planner for students juggling several classes at once. A calendar
tells you *when* something is due; it cannot tell you that three of your
courses have major deliverables in the same week — and that collision is what
turns into a late withdrawal. This app surfaces that collision directly.

## Features

- **Add Assignment** (`pages/1_Add_Assignment.py`) — log an assignment with a
  course, due date, estimated hours, and priority.
- **My Planner** (`pages/2_My_Planner.py`) — everything sorted by due date,
  filterable by course or status, markable as done. Flags any week where two
  or more courses have something due, which is the whole point of the app.

## Running it

```
git clone <repo-url>
cd StudyPlanner
python -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python seed.py
streamlit run app.py
```

If the browser opens and you see seeded assignments, you're set up.

## Dependencies

See `requirements.txt` — Streamlit for the UI, pandas and matplotlib for the
analysis scripts. `sqlite3` ships with Python, so it isn't listed.

## Sample data

`seed.py` creates the tasks table and inserts 8 sample assignments across
three courses. Three of them share a due date on purpose, so the workload
collision the app is built to catch is visible immediately without having to
enter anything by hand.

## Database interface

`db.py` is the single frozen interface both features are built against —
`init_db`, `create_task`, `list_tasks`, `get_task`, `update_status`. Due dates
are always stored as `"YYYY-MM-DD"` strings, never date objects, to avoid a
silent sort-order bug where text-sorted dates don't match calendar order.

## Analysis scripts

`analysis/simulate.py` runs the Monte Carlo cost simulation for the project
report (Part J) — 10,000 trials over development hours, loaded rate, and a
rework multiplier, compared against the project's $30,000 budget. Run it with
`python analysis/simulate.py`; it prints the summary stats and saves
`analysis/cost_distribution.png`.

## AI-Assisted Development

- **Tools used:** Claude (Claude Code), via the Claude Agent SDK.
- **What it helped build:** the `db.py` interface and `seed.py` sample data,
  both Streamlit feature pages, the `analysis/simulate.py` Monte Carlo script,
  and the drafting of the quantitative report sections (NPV, risk register,
  decision tree, Monte Carlo).
- **Where AI-generated code needed a human fix:** nothing has broken in
  testing so far — every function and page passed on first test. The
  candidate to watch during manual/live testing is the collision-flagging
  logic in My Planner: it groups due dates by ISO calendar week (Monday–Sunday),
  so two dates 3 days apart that straddle a week boundary (e.g. a Friday and
  the following Monday) won't be flagged as colliding even though they're
  close together in real time. If that turns out to matter in practice, it's
  a one-line fix to switch to a rolling date-range window instead.
- **A decision the humans made instead of the AI:** in Part I's decision
  tree, the EMV math favored launching campus-wide ($44,000 vs. $42,250 for
  a single-department pilot) — but we chose to recommend the pilot anyway,
  because EMV doesn't capture the tail risk of a FERPA misstep or a trust
  breakdown with students at full campus scale. The math informed the
  decision; it didn't make it.
