# pulse-brownfield-feature-demo

One spec. Two independent agents. A feature implemented into a real existing backend and governed end-to-end by Okto Pulse.

Table of contents
- [Project overview](#project-overview)
- [Quick links](#quick-links)
- [Highlights](#highlights)
- [Repository structure](#repository-structure)
- [Board & demo data](#board--demo-data)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Running the target app](#running-the-target-app)
- [Sprint plan & tasks](#sprint-plan--tasks)
- [Roles & responsibilities](#roles--responsibilities)
- [Tools used](#tools-used)
- [Where to find artifacts](#where-to-find-artifacts)
- [Contributing & licensing](#contributing--licensing)

---

## Project overview

This repository demonstrates adding threaded comment replies with @mention notifications to an existing FastAPI backend (`app/`) while exercising Okto Pulse's governance features. The demo uses two independent AI agents connected to the same Pulse board:
- Builder (Executor): implements code and tests.
- Validator: independently reviews submissions and gates approval.

The repository contains a forked backend, a seeded SQLite board database, and reference exports representing the demo run.

## Quick links
- Web UI (Okto Pulse): http://localhost:8100
- MCP server: http://localhost:8101/mcp
- Target backend: http://localhost:8000 (when running)

## Highlights
- Spec-driven feature: reply threading and @mention resolution implemented from a Pulse spec.
- Two-agent workflow: Builder and Validator identities enforce role separation.
- Validation gate: sprint only closes after independent approval and passing test evidence.

## Repository structure

| Path | Purpose |
| ---- | ------- |
| README.md | This document |
| app/ | Forked FastAPI backend under test |
| app/FORK_NOTES.md | Notes for the fork and build fixes |
| data/pulse.db | Bundled SQLite board for the demo (seed data) |
| docs/ | Walkthrough docs, reference run exports, and images |
| docker-compose.yml | Optional compose for demo services |
| LICENSE | Project license |


## Board & demo data

| Field | Value |
| ----- | ----- |
| Board name | `pulse-brownfield-feature-demo` |
| Board ID | `af285ee4-9a28-4369-bc9a-ac5ab7c75c7b` |
| Target application | `app/` (fork of nsidnev/fastapi-realworld-example-app) |
| Current pipeline checkpoint | Ideation: done (v6), Refinement: done (v4), Spec: approved (v20), Sprints & Cards: N/A |

This snapshot is intended to run the validation gate and exercise the feature in the running app.

## Prerequisites

| Requirement | Notes |
| ----------- | ----- |
| Python 3.11+ | Required by Okto Pulse |
| Two separate agent connections | One Executor (Builder) and one Validator — do not share credentials |
| Docker (optional) | If you prefer containerized Postgres / app runtime |

## Quickstart

1. Install Okto Pulse (CLI & local services):

```bash
pip install okto-pulse
```

2. Initialize a workspace in your project directory:

```bash
okto-pulse init
```

This creates the local data directory (~/.okto-pulse/), a default board and agent, and a project-local .mcp.json pointing agents at the local MCP server.

3. Seed the demo board (copy bundled DB):

```bash
mkdir -p ~/.okto-pulse/data
cp data/pulse.db ~/.okto-pulse/data/pulse.db
```

4. Start the Okto Pulse workbench (Web UI + MCP server):

```bash
okto-pulse serve
```

5. Open the UI at http://localhost:8100, select the `pulse-brownfield-feature-demo` board, and connect two agent identities (Executor and Validator) with separate MCP configs.

## Running the target app (app/)

The `app/` service is a Poetry-managed FastAPI app that runs against PostgreSQL.

1) Install PostgreSQL (15+ recommended). Example macOS (Homebrew):

```bash
brew install postgresql@15
brew services start postgresql@15
```

2) Create the default role and database (example):

```bash
psql postgres -c "CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres' SUPERUSER;"
psql postgres -U postgres -c "CREATE DATABASE rwdb;"
```

3) Install dependencies and start the app:

```bash
cd app
poetry install
cp .env.example .env
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

If you see "ModuleNotFoundError: No module named 'pkg_resources'", install a pinned setuptools inside the poetry environment:

```bash
poetry run pip install "setuptools<81"
```

When running, the backend is available at: http://localhost:8000

## Sprint plan & tasks

Sprint 1 — Comments Threading + Mentions (six work items across four stages):

| Task | Depends on |
| ---- | --------- |
| Migration: add parent_comment_id column + comment_mentions table | — |
| Implement reply threading (create + validation) | Migration |
| Implement @mention parsing/resolution + read paths | Migration |
| Test: Reply threading (create, depth limit, cross-article) | Threading implementation |
| Test: @mentions resolution and listing | Mentions implementation |
| Test: Cascade delete of replies | Threading implementation |

Execution stages:
- Stage 1 — Foundation: migration task (Builder) → Validator review
- Stage 2 — Implementation: Builder implements threading and mentions; Validator reviews each
- Stage 3 — Testing: Builder implements and runs test scenarios
- Stage 4 — Close-out: Validator evaluates and closes sprint; spec marked complete

Path to completion:
- All implementation tasks reviewed & approved
- All tests passing with genuine verification
- Sprint evaluated and closed; spec marked complete

## Roles & responsibilities

| Preset | Can do | Cannot do |
| ------ | ------ | --------- |
| Spec Writer | Own ideation, refinement, and spec content | Cannot move a spec past approved |
| Executor (Builder) | Implement tasks, move cards toward validation | Cannot submit a validation or move a card to done |
| Validator | Submit task/spec validation, move cards validation → done | Does not implement |
| QA | Write test scenarios | Cannot submit any gate |

This demo uses two agent identities: one on the Executor preset (Builder) and one on the Validator preset. Each agent has separate credentials.

## Tools used (sample)

| Tool | Purpose |
| ---- | ------- |
| okto_pulse_get_task_context | Builder pulls a task's requirements and linked spec context |
| okto_pulse_move_card | Move a task through status lifecycle |
| okto_pulse_submit_task_validation | Validator submits confidence/completeness/drift assessment |
| okto_pulse_get_traceability_report | Trace shipped code back to task/spec/decision |
| okto_pulse_get_board_guidelines | Check active governance rules on the board |
| okto_pulse_submit_sprint_evaluation | Close out a sprint once every task clears |

## Where to find artifacts
- data/pulse.db — SQLite database representing the live walkthrough state used by the demo.
- docs/reference-run/ — JSON exports, transcript.md, screenshots, and summary with run metadata and object IDs.
- app/ — FastAPI codebase fork where comments threading and mentions backend extension will be implemented. See `app/FORK_NOTES.md` for fork-specific notes.

## Contributing
If you want to reproduce the demo or iterate on the sprint: fork this repo, seed your local Okto Pulse data as above, and connect your Builder and Validator agent identities.

## License
This repository is provided under the terms of the included LICENSE file.
