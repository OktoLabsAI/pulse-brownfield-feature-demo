# pulse-brownfield-feature-demo

This repository contains the `app/` fork under test, a backed-up SQLite database of the `okto-pulse` walkthrough board, and the corresponding exports representing the current active cycle.

---

## 1. What the Demo Is

A brownfield feature — **threaded replies + @mentions on article comments** — run through Okto Pulse's `ideation → refinement → spec → sprint` pipeline.
- **Board name:** `pulse-brownfield-feature-demo`
- **Board ID:** `af285ee4-9a28-4369-bc9a-ac5ab7c75c7b`
- **Target application:** `app/`, a fork of [nsidnev/fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app) (FastAPI + Postgres RealWorld/Conduit clone).

---

## 2. Current Pipeline State

As of the current run, the board is at the **handoff phase right before validation**:
- **Ideation** is **`done`** (v6).
- **Refinement** is **`done`** (v4).
- **Spec** is **`approved`** (v20) — successfully authored and promoted from `draft` -> `review` -> `approved`.
- **Sprints & Cards** are **`N/A`** (no active tasks created yet).

This state represents the ideal checkpoint to run the validation gate (creating test cards, linking scenarios, executing the curated Spec checklist, and validating the spec).

Full detail, IDs, and version numbers are documented in [`docs/reference-run/summary.md`](docs/reference-run/summary.md).

---

## 3. How to Run Okto Pulse (With Demo DB)

Follow these steps to spin up the Okto Pulse workbench with this repository's pre-populated board data:

### Step 3.1: Install Okto Pulse
Make sure you have Python 3.11+ installed, then install `okto-pulse`:
```bash
pip install okto-pulse
```

### Step 3.2: Initialize and Seed the Database
Copy the demo database backup (`data/pulse.db`) to your local user data directory so Okto Pulse reads it on boot:
```bash
# Create the local data directory if it doesn't exist
mkdir -p ~/.okto-pulse/data

# Copy the database backup
cp data/pulse.db ~/.okto-pulse/data/pulse.db
```

### Step 3.3: Start the Okto Pulse Workbench
Start both the Web UI and the MCP server in a single command:
```bash
okto-pulse serve
```

* **Web UI URL:** [http://localhost:8100](http://localhost:8100) (select the `pulse-brownfield-feature-demo` board).
* **MCP Server URL:** `http://localhost:8101/mcp` (or with API key: `http://localhost:8101/mcp?api_key=...`).

---

## 4. How to Connect a Coding Agent via MCP

To let your AI coding agent (like Claude Code, Claude Desktop, Cursor, or Cline) discover and operate on this board, initialize the agent configuration file in this repository:

```bash
okto-pulse init --agents
```
This generates a `.mcp.json` file in your repository root, which agents use to query board metadata, fetch spec requirements, and update task statuses.

---

## 5. How to Set Up and Run the Target Application (`app/`)

The application under test (`app/`) is a Poetry-managed FastAPI app running against a PostgreSQL database.

### Step 5.1: Install PostgreSQL
Ensure PostgreSQL (version 15+ recommended) is installed and running locally:
```bash
# On macOS (using Homebrew)
brew install postgresql@15
brew services start postgresql@15
```

Create a default role and database matching the configuration:
```bash
# Connect to default postgres and create the user + db
psql postgres -c "CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres' SUPERUSER;"
psql postgres -U postgres -c "CREATE DATABASE rwdb;"
```

### Step 5.2: Install App Dependencies
Navigate into the `app` directory and install the packages using Poetry:
```bash
cd app
poetry install
```

> [!NOTE]
> **Dependency Rot Fix:** If you hit `ModuleNotFoundError: No module named 'pkg_resources'` on startup, it is due to setuptools version changes (v81+ dropped `pkg_resources` which `aiosql` depends[...]
> ```bash
> poetry run pip install "setuptools<81"
> ```

### Step 5.3: Run Database Migrations and Start the Server
Create the `.env` file from the template and start the FastAPI reload server:
```bash
# Copy env variables
cp .env.example .env

# Run migrations
poetry run alembic upgrade head

# Start server
poetry run uvicorn app.main:app --reload
```
The FastAPI backend will now be live on `http://localhost:8000`.

---

## 6. Where to Find Things

- `data/pulse.db` — SQLite database representing the live walkthrough state.
- `docs/reference-run/` — JSON exports of the current board, specs, refinements, ideations, history, and activity logs.
- `app/` — FastAPI codebase fork where the comments threading and mentions backend extension code will be implemented.
- `app/FORK_NOTES.md` — Notes on the environment setup, dependency workarounds, and verification instructions.
