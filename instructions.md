# FutureTool — Backend Code Challenge

## Context

You are a developer at your own start-up, building the backend of the **FutureTool** application. It is a Flask backend called `flask_sqlite_app`, backed by an SQLite database.

The database contains a table `account` with the fields `name`, `password` and `settings`. Two sample users are created automatically the first time the app starts.

The backend **already** handles the following (you do **not** need to build these):

- `POST /admin/accounts` — create a user
- `GET /admin/accounts` — list users
- `DELETE /admin/accounts/<id>` — delete a user
- `GET /admin/reports/settings` — a report aggregating settings usage across all accounts

(These admin URLs would not be exposed externally in production — they are here only to help you set up data.)

Now you want ordinary users — not just admins — to be able to read **their own** settings, securely.

## Working with AI

- You may use any AI assistant you like (Claude, Copilot, ChatGPT, …), as much as you like — that is how we all work now.
- You are accountable for **every line** that lands in the code. Expect questions like *"why does this work?"* and *"what alternatives did you consider?"* about anything you write or paste.
- Verify AI output before accepting it: run the tests, hit the endpoints by hand.
- Think out loud. Your prompts, your checks and your decisions are part of the evaluation — not just the final code.

## Your goal

1. Fix a bug in account creation (Step 1).
2. Let a user read their own settings — and only their own (Step 2).
3. Review how the app handles account credentials, and harden anything that needs it (Step 3).
4. **Stretch goal:** keep the settings report fast at scale (Step 4).

Suggested pacing for a ~60-minute session: Step 1 ≈ 15 min, Step 2 ≈ 20 min, Step 3 ≈ 10 min, Step 4 with whatever time remains. **Not finishing Step 4 is expected and does not fail the challenge.**

## How this is evaluated — start here

Your work is graded by an automatic test suite **and** by the conversation you have with your interviewer along the way. Treat each step's test as its acceptance criteria — but read this carefully:

> **All tests green is not an automatic pass, and a step left red is not an automatic fail.** How you reason about the problem, how you verify your work, and how you explain your decisions are weighed at least as heavily as the final diff.

Run the suite at any time with:

```
poetry run pytest
```

Every acceptance test's name is **prefixed with the step it belongs to**, so `poetry run pytest` shows you at a glance which step each result maps to. Two tests pass from the start — a server health check and the settings report's existing functional test; the other five go green as you complete the steps below.

Recommended workflow:

1. **Run `poetry run pytest` first**, before writing any code, to see the current state.
2. Work **one step at a time**, in the order below, re-running the tests as you go.
3. A step is functionally done when its corresponding test passes. Move on once it is green.

You are free to add or change any application code you need. You are **not** expected to modify the tests. There is nothing to "fix" in the test files themselves — but reading them to learn the exact contract a step expects is fair game and encouraged.

## Step 1 — Fix a bug

A support ticket came in:

> "Sometimes, when creating an account, the API returns `500 Internal Server Error`."

Reproduce it, find the root cause, and fix it so that instead of crashing the API returns a **client error** (a `4xx` status) — and no bad data is left behind.

The Step 1 test is green when this is done.

## Step 2 — Let a user read their own settings

Today anyone can call the admin routes, but an ordinary user has no way to read **their own** settings — and only their own. Build that.

The requirements:

- A user must have a way to **prove who they are** to the backend.
- Given that proof, a user can retrieve their own `settings` value — and must **not** be able to read anyone else's.
- The endpoint that returns a user's settings must be **protected**: no valid proof of identity, no data.

*How* a user proves their identity is your design decision — that choice is part of what we're evaluating, so reach for whatever mechanism you think fits and be ready to defend it.

The precise request/response contract the grader checks (route names, headers, response keys, status codes) is pinned down by the acceptance tests in `tests/test_authentification.py`. Reading those tests to derive the exact contract is expected and legitimate — the point is that the *approach* is yours to choose, not that the details are secret.

## Step 3 — Credentials

Now that a user can log in, read the account model and the account-creation code again — this time as if real users were signing up tomorrow.

Is there anything about the way this app handles account credentials that you would want to change before that happens? If so, make the change, and be ready to explain **why** it matters.

A couple of acceptance notes, so the automated checks stay deterministic:

- The grader inspects the **actual SQLite file** (`src/instance/app.db`), not just your Python — any schema change has to reach the database itself. Because this is a development environment, it is fine to delete `app.db` to apply one.
- If your change touches the `password` column, the grader expects that column to be `VARCHAR(255)` in the database file.
- `werkzeug.security` is installed in your environment and available should you want it.

The two Step 3 tests go green when this is done.

## Step 4 — Stretch goal: keep the settings report fast at scale

Treat this final step as a short product spec and turn it into working code — the way most work arrives now: you're handed intent and constraints, and you decide the implementation.

**Product Requirements — settings report performance**

- **Background:** `GET /admin/reports/settings` returns correct results today, but in production — where there are thousands of accounts — it hammers the database and can take it down.
- **Goal:** the report stays responsive as the number of accounts grows, while returning exactly the same output.
- **Requirements:**
  - **R1** — The response body is byte-for-byte unchanged, and the report's existing functional test stays green.
  - **R2** — The endpoint issues a small, **constant** number of `SELECT` queries; the query count must not grow with the number of accounts.
  - **R3** — It responds in well under a couple of seconds at a few thousand accounts.
- **Out of scope:** caching, new endpoints, pagination, or any change to the response shape.
- **Acceptance:** the Step 4 performance test passes and the report's functional test still passes.

Running out of time here is normal: this step exists to see how far you get, not to gate the challenge.

## Environment & commands

Run these from the project root:

- **Install dependencies:** `poetry install`
- **Run the tests (acceptance criteria):** `poetry run pytest`
- **Start / restart the server:** `poetry run myserver`

The SQLite database file lives at `src/instance/app.db`.
