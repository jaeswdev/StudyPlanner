# Study Planner

CMPE 165 · Project 1 — **Hyunjae(Henry) Lee** & **Anahi Carrasco**
San José State University, Fall 2026

## What this is

A course-load planner for students taking several classes at once.

A calendar tells you _when_ something is due. It cannot tell you that three of your
courses have unfinished work landing in the same week — and that collision is what turns
into a late withdrawal. This app surfaces that collision directly.

The intended customer is a university Student Success Center. The value is **student
retention**, not personal convenience.

## Major features

- **Add Assignment** (`pages/1_Add_Assignment.py`) — log an assignment with its course,
  due date, estimated hours, and priority. Input is validated before it reaches the
  database.
- **My Planner** (`pages/2_My_Planner.py`) — every assignment sorted by due date, then by
  priority, filterable by course or status, and markable as done. It flags any
  Monday–Sunday week in which **three or more courses** have unfinished work due, naming
  the courses involved. Marking work done can clear a week's warning, because finished
  work no longer counts toward a collision.

## Running it

Requires Python 3.9 or newer. On macOS use `python3`; bare `python` does not exist there.

```bash
git clone https://github.com/jaeswdev/StudyPlanner.git
cd StudyPlanner
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python3 seed.py
streamlit run app.py
```

If the browser opens at `http://localhost:8501` and you can see seeded assignments,
you are set up.

To reset to a clean state at any point:

```bash
rm -f planner.db && python3 seed.py
```

Use `rm -f` rather than `rm` — if the file is already gone, plain `rm` fails and `&&`
skips the seed.

## Required packages and dependencies

See `requirements.txt` — **Streamlit** for the user interface and **matplotlib** for the
chart produced by `analysis/simulate.py`. `sqlite3` is part of the Python standard
library, so it is not listed and needs no installation.

Verified against Python 3.9.6 and Streamlit 1.50.0.

## Sample data

`seed.py` creates the `tasks` table and inserts 8 sample assignments across three
courses. Dates are generated relative to the coming Monday, so they are always in the
future no matter when the script is run.

Three of those assignments deliberately fall in the same Monday–Sunday week — 17 hours of
work across CMPE 165, CS 149 and CS 157A — so the workload collision the app exists to
catch is visible immediately without entering anything by hand. The following week
contains only two courses, so it is correctly left unflagged.

Re-running `seed.py` against a database that already has rows inserts nothing, so it is
safe to run twice.

## Database interface

`db.py` is a single frozen interface that both feature pages are built against. It
exposes exactly five public functions:

```python
init_db()
create_task(title, course, due_date, est_hours, priority)   # returns the new id
list_tasks(course=None, status=None)
get_task(task_id)
update_status(task_id, status)
```

Every task is returned as a dictionary with exactly these keys: `id`, `title`, `course`,
`due_date`, `est_hours`, `priority`, `status`, `created_at`.

`priority` is one of `"Low"`, `"Medium"`, `"High"`; `status` is one of `"Not Started"`,
`"In Progress"`, `"Done"`. Both are exported as the tuples `db.PRIORITIES` and
`db.STATUSES` so that no page file has to retype them.

**Due dates are always stored as `"YYYY-MM-DD"` strings.** SQLite has no date type — it
stores whatever it is given as text, without complaint — and `"YYYY-MM-DD"` is the only
common format whose text ordering matches calendar ordering. `create_task()` accepts a
`date`, a `datetime`, or a correctly formatted string and normalises all three; anything
else raises an error rather than being stored. The table also carries CHECK constraints on
`priority` and `status`, so an incorrectly capitalised value fails loudly at the boundary
instead of producing a silently empty filter result.

Freezing this interface before either feature was written was a deliberate choice, and it
is the reason the two pages could be developed in parallel without conflicting.

## Analysis scripts

`analysis/simulate.py` runs the Monte Carlo cost simulation used in the project report —
10,000 trials over three uncertain variables: development hours (triangular), a
fully-loaded hourly rate (uniform), and a rework multiplier (uniform), compared against a
$30,000 budget.

Run it **from the repository root**, since the chart path is relative:

```bash
python3 analysis/simulate.py
```

It prints summary statistics and saves `analysis/cost_distribution.png`. The random seed
is fixed at 42, so the figures are reproducible:

```
trials          10,000
mean cost       $30,290
P10 (best case) $24,423
P90 (worst case)$36,631
P(over budget)  50.0%   (budget = $30,000)
```

## AI-Assisted Development

**Which AI coding tools we used.** Claude, through Claude Code in the terminal, for
essentially all of the implementation work. We also used Claude in chat to plan the split
of work and to review the code afterwards.

**What the AI helped us build.** The `db.py` data layer and its validation, `seed.py` and
its sample data, both Streamlit feature pages, the `analysis/simulate.py` Monte Carlo
script, and the drafting of the quantitative sections of the report. Most of it worked on
the first attempt, which is the honest assessment — the interesting failures were not
about the AI writing incorrect logic.

**One example where AI-generated code did not work and had to be modified.** The version
of `db.py` that first reached `main` used modern type-hint syntax in its function
signatures — `str | None` — which is the union syntax introduced in Python 3.10. The
project's virtual environment on the Mac was built from the system Python, version 3.9.6,
where that syntax raises a `TypeError` the moment the module is imported. Every page
therefore failed to load.

What made this expensive rather than obvious was _where_ it hid. The code was correct
Python on the machine it was written on, because that machine had a newer interpreter. It
only failed on the target environment. No amount of reading the code would have caught
it; running it on the actual Python we intended to ship against is what caught it. We
replaced that file with a 3.9-compatible implementation, delivered as a pull request so
the other team member had to review and merge it rather than it going straight to `main`.

A second, blunter failure the same evening: `db.py` was committed at zero bytes, because
its contents had been pasted into `app.py` instead. The symptom was an `ImportError`
rather than a `ModuleNotFoundError` — Python found the module and it was simply empty —
which is a distinction worth knowing, because it points at the file's contents rather
than its location.

**One important decision the human team made rather than the AI.** Two of them.

The first was procedural. Both of us had independently written and pushed a file we each
considered the "frozen" `db.py`, so the shared interface existed in two incompatible
versions at once. No tool resolved that; we had to decide which implementation became
canonical, and then chose to route it through a pull request requiring the other person's
approval instead of pushing the fix directly. That cost a few minutes and removed the
possibility of a third version appearing.

The second was a judgement call against the arithmetic. In the report's decision-tree
analysis, expected monetary value favoured a campus-wide launch ($44,000) over a
single-department pilot ($42,250). We recommended the pilot anyway. Expected value is an
average over many repetitions, and this project runs once; it does not price the tail risk
of a FERPA misstep or of losing student trust at full scale. The math informed the
decision. It did not make it.
