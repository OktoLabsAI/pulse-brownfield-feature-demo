# pulse-brownfield-feature-demo — Scenario Walkthrough

Scenario: You are a developer tasked with validating and integrating a brownfield feature — threaded replies and @mentions on article comments — into an existing RealWorld-style app. This repository contains everything you need to run the Okto Pulse board and the target app so you can reproduce the pipeline, run the validation gate, and exercise the feature end-to-end.

---

## The Setup (what's in this repo)

- `app/` — a fork of [nsidnev/fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app). This is the target application where the comments threading + mentions backend changes will be implemented and verified.
- `data/pulse.db` — a backed-up SQLite database representing a pre-populated Okto Pulse board matching the demo scenario.
- `docs/reference-run/` — JSON exports and a summary of the board, specs, ideations, refinements, and run history.

Board details used in the scenario:
- Board name: `pulse-brownfield-feature-demo`
- Board ID: `af285ee4-9a28-4369-bc9a-ac5ab7c75c7b`
- Target application: `app/` (FastAPI + Postgres RealWorld/Conduit clone)

---

## Scenario goal

You will take the board from the handoff phase into validation, create test cards, link scenarios, run the curated Spec checklist, and validate the acceptance criteria for threaded replies and @mentions on article comments.

Current pipeline checkpoint (this repo snapshot):
- Ideation: done (v6)
- Refinement: done (v4)
- Spec: approved (v20)
- Sprints & Cards: N/A (no active tasks yet)

This is the ideal point to run the validation gate and exercise the feature in the running app.

Full IDs and versions are available in `docs/reference-run/summary.md`.

---

## Walkthrough — run the demo (steps to reproduce)

1) Install Okto Pulse

Make sure you have Python 3.11+ and install the CLI/workbench:

```bash
pip install okto-pulse
```

2) Seed the demo Okto Pulse database

Copy the bundled SQLite demo data into your local Okto Pulse data directory so the workbench boots with the pre-populated board:

```bash
mkdir -p ~/.okto-pulse/data
cp data/pulse.db ~/.okto-pulse/data/pulse.db
```

3) Start the Okto Pulse workbench

This starts both the Web UI and the MCP server:

```bash
okto-pulse serve
```

- Web UI: http://localhost:8100 — select the `pulse-brownfield-feature-demo` board.
- MCP API: http://localhost:8101/mcp (append `?api_key=...` if using an API key).

4) Connect a coding agent (optional)

If you want to let an AI coding agent interact with the board via MCP, initialize the agent config in this repository:

```bash
okto-pulse init --agents
```

This creates a `.mcp.json` file which agents use to query board metadata, fetch spec requirements, and update tasks.

5) Prepare and run the target application (`app/`)

The `app/` service is a Poetry-managed FastAPI backend running against PostgreSQL. Follow these steps to run it locally.

- Install PostgreSQL (15+ recommended). Example for macOS (Homebrew):

```bash
brew install postgresql@15
brew services start postgresql@15
```

- Create the default role and database used by the app:

```bash
psql postgres -c "CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres' SUPERUSER;"
psql postgres -U postgres -c "CREATE DATABASE rwdb;"
```

- Install Python dependencies and start the app:

```bash
cd app
poetry install
cp .env.example .env
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

The backend will be available at: http://localhost:8000

Note: If you encounter `ModuleNotFoundError: No module named 'pkg_resources'`, install an older setuptools pinned in your environment:

```bash
poetry run pip install "setuptools<81"
```

---

## What to test (acceptance checklist — scenario steps)

1) Setup verification
- Confirm the `pulse-brownfield-feature-demo` board appears in the Okto Pulse Web UI and matches the board ID above.
- Confirm `app/` starts and its API responds at `/` and the database migrations ran successfully.

2) Create validation artifacts in Okto Pulse
- From the board Spec (approved v20), create one or more Test Cards that represent realistic user scenarios for threaded replies and @mentions (examples below).
- Link each Test Card to the Spec checklist items and ensure the Spec checklist can be executed by an agent or test runner.

3) Execute scenarios against the running app
- Manual or automated tests should exercise the following example scenarios:
  - Post an article comment, reply to it (single-level thread), and verify replies are correctly associated with the parent comment.
  - Create nested replies (2+ levels) and verify thread ancestry is preserved and returned by the API.
  - Mention an existing user in a comment using `@username` and verify the mention is recorded and the API returns structured mention metadata (user id, username, and text offsets if applicable).
  - Verify that notifications or mention hooks (if present) are triggered appropriately when a user is mentioned.

4) Validate and promote results
- When the Test Cards pass, mark them complete and record the validation outcome on the board.
- If failures occur, create follow-up tasks in the board, link to failing scenarios, and iterate until validation passes.

---

## Where to look and debug

- `data/pulse.db` — the SQLite demo board state used by Okto Pulse.
- `docs/reference-run/` — JSON exports and `summary.md` with run metadata and exact object IDs.
- `app/` — the FastAPI codebase under test. See `app/FORK_NOTES.md` for fork-specific notes and dependency workarounds.

---

If you'd like, I can update the README in the repository now with this scenario-style wording. Tell me to proceed and I'll commit the change, or ask for edits to the scenario or checklist before I commit.
