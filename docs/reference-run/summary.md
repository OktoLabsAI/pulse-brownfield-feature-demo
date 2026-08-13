# pulse-brownfield-feature-demo — pipeline export

Board: `pulse-brownfield-feature-demo` (`af285ee4-9a28-4369-bc9a-ac5ab7c75c7b`)
Snapshot taken: 2026-08-13 (current session live status)

The board contains the active pipeline for the feature: **"Threaded Replies + @Mentions for Article Comments"**.

## Current Active Cycle State

| Stage | ID | Status | Version | Description |
|---|---|---|---|---|
| Ideation | `31430bea-1fd4-47fa-952b-c0e7d054c241` | `done` | 6 | "Threaded Replies + @Mentions for Article Comments" |
| Refinement | `c3a74bd6-8b70-41b6-8607-658830a449e6` | `done` | 4 | "Comments Threading + Mentions — Data Model & API Refinement" |
| Spec | `bc153ebb-9ab2-4f12-b9a9-cd6cd7a25248` | `approved` | 20 | "Comments Threading + Mentions — Data Model & API Refinement" |
| Sprint | N/A | N/A | N/A | No active sprints (spec not yet validated/in_progress) |
| Cards | N/A | N/A | N/A | No active cards (spec not yet validated/in_progress) |

## Walkthrough Phase & Handoff

The spec is currently in the **`approved`** status. According to the Okto Pulse core SDLC rules:
1. Sprints and implementation cards cannot be created or started until the spec reaches `approved` or later.
2. Promoting the spec from `approved` to `validated` is gated by the **Spec Validation Gate** (`okto_pulse_submit_spec_validation`).
3. To satisfy the Spec Validation Gate:
   - Create test cards (`card_type="test"`) and link them to the spec's test scenarios until `scenario_task_linkage_pct = 100`.
   - Run the curated checklist template if configured on the board (via `okto_pulse_start_checklist_execution` and `okto_pulse_submit_checklist_execution`).
   - Call `okto_pulse_submit_spec_validation` to lock the spec content and move it to `validated`.
4. Promoting the spec from `validated` to `in_progress` requires executing qualitative evaluation via `okto_pulse_submit_spec_evaluation` (recommending `approve`).

## Files in this directory

- `board.json` — the board row
- `ideations.json`, `refinements.json`, `specs.json`, `sprints.json`, `cards.json` — full rows for the current cycle
- `ideation_history.json`, `refinement_history.json`, `spec_history.json`, `sprint_history.json` — full audit trail per stage (version bumps, status changes, evaluations)
- `activity_logs.json` — full board activity feed
- `agent_boards.json`, `agents.json` — agent access grants and the granted agents' own rows
