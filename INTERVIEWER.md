# FutureTool Challenge — Interviewer Guide

**Do not share this file or any part of it with candidates.** Candidates receive the bundle produced by `make candidate-bundle`, which excludes it.

## Session logistics

- **Format:** live, ~60 minutes, candidate shares their screen and drives.
- **AI:** allowed and encouraged — any assistant (Claude, Copilot, ChatGPT, …). The candidate was told, in `instructions.md`, that they are accountable for every line and should expect probing questions. Hold them to it.
- **Opening (first 5 minutes):** introduce yourself, confirm the environment works (`poetry run pytest` → `2 passed, 5 failed`), point them at `instructions.md`, and say explicitly: *"Use AI as much as you like — I'll ask questions about whatever lands in the code."*
- Release the steps conversationally. Don't let a candidate burn 10 minutes reading everything: after the environment check, steer them to Step 1.
- **Clock:** Step 1 ≈ 15 min, Step 2 ≈ 20 min, Step 3 ≈ 10 min, Step 4 with the remainder. If a candidate is stuck past a step's budget, give a nudge and note it — a nudge is data, not a failure.

## Rubric

Score each competency 1–4 (1 = clear no, 2 = below bar, 3 = at bar, 4 = above bar). These are the same four competencies Meta uses in its AI-enabled interviews.

| Competency | Strong signal (examples) | Red flag (examples) |
| --- | --- | --- |
| **Problem solving** | Reproduces the bug before touching code; reads the failing test to derive the scenario; spots the N+1 unaided | Pastes the error into AI without reading any code; cannot state the root cause of the bug they just "fixed" |
| **Code quality** | New code matches the project's existing style and structure; errors handled where they occur | Accepts AI output whose style/patterns are alien to the project; dead code and unused imports pasted in |
| **Verification** | Runs pytest after each change; hits endpoints by hand; reads AI output before accepting it | Declares a step done without running anything; trusts AI output unchecked |
| **Communication** | Narrates the plan before acting; asks the AI rich, specific questions; explains trade-offs unprompted | Long opaque silences; "fix this" prompts; cannot explain code they pasted |

## Probing questions per step

**Rule of use: at least one probe per completed step, and always when AI-generated code is pasted.** A candidate who answers well has validated their AI use. One who cannot exposes the central red flag: relying on AI they don't understand.

**Step 1 — bug fix** (expected fix: catch `IntegrityError` in the account service, roll the session back, return 4xx)
- "Why did this return 500 and not 400 before your fix?"
- "What state is the SQLAlchemy session in after an `IntegrityError`? What happens if you catch the exception but don't roll back?" *(this is the depth layer — a `try/except` without `db.session.rollback()` breaks subsequent DB operations)*
- "You could also check-then-insert. What's the race condition there?"

Note: the ticket in `instructions.md` is deliberately vague, but the failing test's name reveals the duplicate-name scenario — that breadcrumb is intended. Finding the cause by reading the test is at-bar problem solving, not a shortcut.

**Step 2 — token auth**
- "JWT versus an opaque token stored in the DB — trade-offs?"
- "Where does your token expire? What happens if it never does?"
- "If I steal the `Authorization` header, what can I do? What would limit the damage?"

**Step 3 — password hashing**
- "Why a salted hash instead of plain SHA-256?"
- "What does `werkzeug.security.generate_password_hash` use underneath?"
- "Why did the column need to grow to 255?"

**Step 4 — report optimization** (expected fix: one query — e.g. load all settings in a single `SELECT`, aggregate in Python, or aggregate in SQL)
- "What exactly made it slow? What's an N+1 query?"
- "How would you detect this in production before users complain?"
- "With 10 million accounts, does your one-query version still work? What next?"

## Level calibration

- **Mid-level bar:** Steps 1–3 complete with solid probe answers. Step 4 not reached is fine.
- **Senior bar:** Steps 1–3 with depth on the probes (e.g. names the session-rollback issue unprompted, discusses token trade-offs fluently) **and** meaningful progress on Step 4 — at minimum a correct diagnosis of the N+1.
- Not finishing Step 4 never fails a candidate on its own. Meta's data point: candidates who ran out of time but reasoned soundly still got offers.
- A candidate whose tests are all green but who fails multiple probes is **below** the bar of one with a red Step 4 and sharp answers. The artifact is not the assessment; the conversation is.

## Producing the candidate bundle

```bash
make candidate-bundle
```

This creates `candidate-bundle.zip` from the latest commit, excluding this file, `docs/`, `.superpowers/` and the `Makefile`. Send the candidate the zip, never the repo. If you change the challenge, re-run the target — it always reflects `HEAD`. If you add new interviewer-only files to the repo, add matching excludes to the `Makefile` — the bundle only excludes the paths listed there.
