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

Now you want users to be able to **log in** and **retrieve their own settings**.

## Working with AI

- You may use any AI assistant you like (Claude, Copilot, ChatGPT, …), as much as you like — that is how we all work now.
- You are accountable for **every line** that lands in the code. Expect questions like *"why does this work?"* and *"what alternatives did you consider?"* about anything you write or paste.
- Verify AI output before accepting it: run the tests, hit the endpoints by hand.
- Think out loud. Your prompts, your checks and your decisions are part of the evaluation — not just the final code.

## Your goal

1. Fix a bug in account creation (Step 1).
2. Add token-based authentication so a user can log in and read their settings (Step 2).
3. Store passwords securely as hashes instead of clear text (Step 3).
4. **Stretch goal:** make the settings report fast (Step 4).

Suggested pacing for a ~60-minute session: Step 1 ≈ 15 min, Step 2 ≈ 20 min, Step 3 ≈ 10 min, Step 4 with whatever time remains. **Not finishing Step 4 is expected and does not fail the challenge.**

## How this is evaluated — start here

Your work is graded by an automatic test suite **and** by the conversation you have with your interviewer along the way. The tests are the acceptance criteria for each step — when a step's test passes, the step is functionally done.

Run them at any time with:

```
poetry run pytest
```

Recommended workflow:

1. **Run `poetry run pytest` first**, before writing any code, to see the current state. Two tests already pass; the others fail until you complete the steps below.
2. Work **one step at a time**, in the order below, re-running the tests as you go.
3. A step is done when its corresponding test passes. Move on once it is green.

You are free to add or change any application code you need. You are **not** expected to modify the tests. There is nothing to "fix" in the test files themselves.

| Failing test | What makes it pass |
| --- | --- |
| `test_duplicate_name_rejected` | Step 1 — fix the account-creation bug |
| `test_register_and_login` | Step 2 — create `POST /login` and `GET /settings` |
| `test_db_field_size` | Step 3, Part A — enlarge the `password` field to 255 |
| `test_password_storage` | Step 3, Part B — hash and verify passwords |
| `test_report_performance` | Step 4 — optimize the settings report |

(`test_simple`, the health check, and `test_report_settings`, the report's functional test, pass from the start.)

## Step 1 — Fix a bug

A support ticket came in:

> "Sometimes, when creating an account, the API returns `500 Internal Server Error`."

Reproduce it, find the root cause, and fix it so that instead of crashing the API returns a **client error** (a `4xx` status) — and no bad data is left behind.

The test `test_duplicate_name_rejected` is green when this is done.

## Step 2 — Token authentication

Implement two new routes. **Neither of them exists yet — you need to create them.**

**Log in — `POST /login`**

- Request body: a JSON object with the keys `name` and `password`.
- If the password is correct: respond with status `200` and a JSON body containing the key `token`, set to an authentication token.
- The token must let the backend identify *which* user is logged in on later requests.

**Read settings — `GET /settings`**

- The request must include an `Authorization` header set to `Bearer <token>`, where `<token>` is the token returned by `/login`.
- If the token is valid: respond with a JSON body containing the key `settings`, set to that user's `settings` value from the database.

To create a user for manual testing, use the existing `POST /admin/accounts` route (see Context above).

## Step 3 — Secure password storage

Passwords are currently stored as clear text, which is bad practice. This step has two parts.

**Part A — Enlarge the `password` field**

The `password` column is too short to hold a password hash. Change its length from `100` to `255`.

> ⚠️ The grader checks the **actual column size in the SQLite file**, not just in your code. Make sure the change is reflected in the database itself.

Because this is a development environment, it is fine to delete all existing data in the database to apply the change.

**Part B — Hash the passwords**

Update the backend so that:

- Passwords are stored as **hashes** when a user is created.
- Login verifies the submitted password against the stored hash (correct password → `200`, wrong password → non-`200`).

It is recommended to use `werkzeug.security`, which is already installed in your environment.

## Step 4 — Stretch goal: optimize the settings report

The settings report (`GET /admin/reports/settings`) works and its functional test passes. But the infra team complains that in production — where there are thousands of accounts — this report takes the database down.

Find out why, and optimize it without changing what it returns.

The test `test_report_performance` is green when this is done. Running out of time here is normal: this step exists to see how far you get, not to gate the challenge.

## Environment & commands

Run these from the project root:

- **Install dependencies:** `poetry install`
- **Run the tests (acceptance criteria):** `poetry run pytest`
- **Start / restart the server:** `poetry run myserver`

The SQLite database file lives at `src/instance/app.db`.
