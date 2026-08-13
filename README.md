
One spec. Two independent agents. A board that won't let either one mark its own homework done.
A real feature — threaded comment replies with @mention notifications — built on a real existing codebase, governed end-to-end by Okto Pulse.

About OktoLabs · About Okto Pulse · The Problem · How It Works · Architecture · Repository Structure · Roles · Tools · Quickstart · Sprint Stages · Conclusion

About OktoLabs
OktoLabs is a small team building developer tooling for AI-assisted software delivery. Their public work is organized under the OktoLabsAI GitHub organization, currently six repositories:

Repo
What it is
okto-pulse
The main product — a governed SDLC workbench for AI coding agents
okto-pulse-core
The domain layer Pulse is built on (specs, gates, knowledge graph contracts)
docs
Okto Pulse's public documentation site
claude-plugins
OktoLabs' marketplace for Claude Code plugins
mcp-replay-test
Tooling for replaying and testing MCP interactions
marginalia-dist
Internal distribution tooling

OktoLabs' focus across all of it is the same: as AI agents write more of the actual code, someone still needs a system that keeps requirements, decisions, and delivery evidence connected — instead of trusting an agent's own summary of what it did.

About Okto Pulse
Okto Pulse is a local-first SDLC workbench — it runs on your own machine, no account required — built for teams using AI coding agents who still want to be able to trace why something was built the way it was, and prove it was actually finished correctly.
In plain terms: instead of an agent going straight from "here's an idea" to "here's the code," Pulse keeps every step explicit and connected —
Stories → Ideation → Refinement → Spec → Sprint → Tasks / Tests / Bugs

Every one of those stages produces a real, structured record — not just a chat transcript that disappears. Requirements, decisions, and test evidence stay linked to each other, so months later, "why does this work this way" has an actual answer. Agents interact with all of this through MCP; humans can look at the exact same board in a web UI.

The Problem
AI coding agents are good at producing an implementation. They're not naturally good at proving that implementation actually satisfies what was asked — especially on a codebase that already has its own history and conventions.
Three specific failure modes this repo is built to test directly, not just describe:
Status can drift from reality. A card can be marked "done," a sprint can close, tests can be marked "passed" — while the underlying code was never actually written. Nothing about a status label guarantees it's true.
Self-review isn't review. If the same agent that writes a card is also the one that approves it, "approved" just means "the agent still agrees with itself."
A rule nobody enforces is a suggestion. A guideline that only warns doesn't stop bad work from shipping — it just leaves a note next to it on the way out.
Pulse is built with governance gates specifically meant to close these gaps. This repo doesn't take that at face value — it pushes on each one directly, on a real feature, and reports what actually happened.

How It Works
This repo adds threaded comment replies with @mention notifications to an existing backend API, using two independent AI agents connected to the same Pulse board:

Spec first. The feature — a self-referencing parent_comment_id, a comment_mentions table, reply threading, and @mention resolution — is fully specified in Pulse and validated before any implementation task is opened.
Builder implements. One agent works through each implementation task: reviewing requirements, writing the code, and submitting the task for review with a completeness estimate and any noted deviation from spec.
Validator checks independently. A separate agent reviews each submission — for confidence, completeness, and drift from spec — and approves or sends it back with a reason. A submission that falls short on any of those three is not approved, regardless of what the builder claims.
Tests are run, not just written. Test tasks require the scenario to actually execute and pass — automated execution alone isn't accepted as evidence.
The sprint only closes when every task genuinely clears. All implementation tasks approved, all test scenarios passing, the sprint evaluated and closed, the spec marked complete — in that order, not asserted out of order.

Architecture

(Diagram pending — showing the Builder and Validator agents connected to the same Pulse board over MCP, the spec → sprint → task lineage, and where the validation gate sits between "submitted" and "done.")

Repository Structure
pulse-brownfield-feature-demo/
├── README.md
├── app/                                # the existing backend the feature is built into
│   └── FORK_NOTES.md                   # what was patched to get it building today
├── docs/
│   ├── decisions/                      # recorded pre-existing conventions (e.g. auth scheme)
│   ├── images/
│   │   ├── hero.svg
│   │   └── architecture-placeholder.svg
│   ├── pulse-walkthrough/
│   │   ├── 00-setup.md
│   │   ├── 01-ideation.md
│   │   ├── 02-refinement.md
│   │   ├── 03-spec.md
│   │   ├── 04-sprint-and-tasks.md
│   │   ├── 05-implementation.md
│   │   ├── 06-validation.md
│   │   └── 07-closeout.md
│   └── reference-run/
│       ├── transcript.md
│       └── screenshots/
├── docker-compose.yml
└── LICENSE

This repository contains the `app/` fork under test, a backed-up SQLite database of the `okto-pulse` walkthrough board, and the corresponding exports representing the current active cycle.

Board details used in the demo:
- Board name: `pulse-brownfield-feature-demo`
- Board ID: `af285ee4-9a28-4369-bc9a-ac5ab7c75c7b`
- Target application: `app/`, a fork of nsidnev/fastapi-realworld-example-app (FastAPI + Postgres RealWorld/Conduit clone)

Current pipeline checkpoint (this repo snapshot):
- Ideation: done (v6)
- Refinement: done (v4)
- Spec: approved (v20)
- Sprints & Cards: N/A (no active tasks yet)

This is the ideal point to run the validation gate and exercise the feature in the running app.

Roles
Okto Pulse enforces role separation through permission presets — not just instructions either agent could ignore. Four presets exist on the platform:

Preset | Can do | Cannot do
Spec Writer | Owns ideation, refinement, and spec content | Cannot move a spec past approved
Executor (Builder, this repo) | Implements tasks, moves cards toward validation | Cannot submit a validation or move a card to done
Validator (this repo) | Submits task/spec validation, moves cards validation → done | Does not implement
QA | Writes test scenarios | Cannot submit any gate

This repo uses two agent identities specifically: one on the Executor preset (the Builder), one on the Validator preset. Each is a separate connection with its own credentials — not a shared identity switching roles, since that would defeat the separation at the connection level, not just the permission level.

Tools Used
A sample of the real MCP tools this workflow runs on (Okto Pulse currently exposes a broad set of MCP tools over okto-pulse serve):

Tool | Used for
okto_pulse_get_task_context | Builder pulls a task's requirements and linked spec context before implementing
okto_pulse_move_card | Moving a task through its status lifecycle
okto_pulse_submit_task_validation | Validator submits a confidence/completeness/drift assessment
okto_pulse_get_traceability_report | Tracing shipped code back through its task, spec, and originating decision
okto_pulse_get_board_guidelines | Checking what governance rules are actually active on the board
okto_pulse_submit_sprint_evaluation | Closing out the sprint once every task clears

Prerequisites
Requirement | Notes
Python 3.11+ | Required by Okto Pulse
Two separate agent connections | One Executor, one Validator — do not share credentials between them
Docker (optional) | If running the target app in a container

Quickstart
Sourced directly from Okto Pulse's own install steps and aligned to this repo's demo data.

1. Install

```bash
pip install okto-pulse
```

2. Initialize a workspace

Run this inside the project directory your agents will work from:

```bash
okto-pulse init
```

This creates the local data directory under ~/.okto-pulse/, a default board and agent, and a project-local .mcp.json pointing your agent at the local MCP server.

3. Seed the demo board (copy bundled DB)

```bash
mkdir -p ~/.okto-pulse/data
cp data/pulse.db ~/.okto-pulse/data/pulse.db
```

4. Start the app

Start the Okto Pulse workbench (Web UI + MCP server):

```bash
okto-pulse serve
```

Endpoints
Web UI + API: http://localhost:8100
MCP server: http://localhost:8101/mcp

4. Open the UI
Go to http://localhost:8100, select the `pulse-brownfield-feature-demo` board, and connect your two agent identities — one Executor, one Validator — each with its own generated MCP config.

Where to find implementation and run artifacts
- `data/pulse.db` — SQLite database representing the live walkthrough state used by the demo.
- `docs/reference-run/` — JSON exports and `summary.md` with run metadata and exact object IDs.
- `app/` — the FastAPI codebase fork where the comments threading and mentions backend extension code will be implemented. See `app/FORK_NOTES.md` for fork-specific notes and dependency workarounds.

How to run the target app (`app/`)
The application under test (`app/`) is a Poetry-managed FastAPI app running against a PostgreSQL database.

1) Install PostgreSQL (15+ recommended). Example for macOS (Homebrew):

```bash
brew install postgresql@15
brew services start postgresql@15
```

2) Create the default role and database matching the configuration:

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

The backend will be available at: http://localhost:8000

Note: If you encounter `ModuleNotFoundError: No module named 'pkg_resources'`, install an older setuptools pinned in your environment:

```bash
poetry run pip install "setuptools<81"
```

Sprint Stages
This is the actual execution plan this repo's Sprint 1 (Comments Threading + Mentions) runs on, six work items across four sequential stages.

The six tasks
Task | Depends on
Migration: parent_comment_id column + comment_mentions table | — (start here)
Implement reply threading (create + validation) | Migration
Implement @mention parsing/resolution + read paths | Migration
Test: Reply threading (create, depth limit, cross-article) | Threading implementation
Test: @mentions resolution and listing | Mentions implementation
Test: Cascade delete of replies | Threading implementation

Builder responsibilities
For each implementation task: review the task's requirements and any linked material before starting, move it through its stages as work progresses, and on completion submit it for review with a summary of what was built, a completeness estimate, and any deviation from spec.
For each test task: implement and run the assigned scenario(s), and only record a result as passed once it's actually been verified — automated execution alone isn't sufficient.

Validator responsibilities
Review every submitted implementation task independently of whoever built it. Assess confidence in the result, completeness against requirements, and drift from spec. Approve, or request changes with a clear reason. A submission that falls short on confidence, completeness, or drift is not approved, regardless of what the builder's own recommendation says.

Execution order
Work proceeds in four sequential stages; within a stage, tasks can run in any order or in parallel.

Stage 1 — Foundation
Prompt the Builder on the migration task.
Prompt the Validator to review it once submitted.

Stage 2 — Implementation (both tasks depend only on the migration; can run in parallel)
Prompt the Builder on reply threading.
Prompt the Builder on @mentions.
Prompt the Validator to review reply threading.
Prompt the Validator to review @mentions.

Stage 3 — Testing (each test depends on its matching Stage 2 implementation)
Prompt the Builder on the reply threading test.
Prompt the Builder on the @mentions test.
Prompt the Builder on the cascade delete test.

Stage 4 — Close-out
Prompt the Validator to evaluate and close the sprint once every implementation task is approved and every test is passing.
Mark the specification complete.

Path to completion
All three implementation tasks reviewed and approved.
All three test tasks have their scenarios genuinely passing.
The sprint is submitted for evaluation and closed on approval.
The specification is marked complete only once all sprint work is closed out.

Built on Okto Pulse, an OktoLabs product.
