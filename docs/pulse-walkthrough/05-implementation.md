# 05 — Implementation

## Status

**Pulse-side pipeline: complete.** On board `pulse-brownfield-feature-demo`
(`af285ee4-9a28-4369-bc9a-ac5ab7c75c7b`), for the "Threaded Replies +
@Mentions for Article Comments" feature:

| Entity | ID | Status |
|---|---|---|
| Ideation | `046cac6a-4bb1-42af-8822-b2b21cfbbe9e` | done (v7) |
| Refinement | `8d4d8a2e-1da1-4326-884b-eaee6a04a469` | done (v5) |
| Spec | `6a929f8b-03b1-4563-9dad-2faa6c78b336` (edition 1) | done (v42) |
| Sprint | `2b365a63-a43e-4559-8390-602e4ba80388` ("Sprint 1 — Comments Threading + Mentions") | closed |

All 6 cards on the sprint are `done`, and all 7 linked test scenarios
(`ts_2d77eef0`, `ts_279a5ba6`, `ts_bb32e991`, `ts_21372116`, `ts_51265314`,
`ts_faf62837`, `ts_4db605b1`) carry `status: passed` with an
`mcp_replay_manifest` execution attestation (producer
`okto-pulse-community` v0.3.1).

**Important — actual repo code is unmodified.** As of this writing,
`grep -r "parent_comment_id\|comment_mentions\|mentioned_user_id" app/`
returns zero matches in the forked app (`nsidnev/fastapi-realworld-example-app`
at `app/`). The migration
(`commentaries.parent_comment_id`, new `comment_mentions` table), the
API changes to `POST`/`GET /api/articles/{slug}/comments`, and the
mention-parsing logic described in the spec's `technical_requirements`
and `api_contracts` have **not** been written to `app/` yet. The test
scenarios' `passed` evidence is a Pulse-side replay/health-check
attestation (`health.http_status`, `health.status_healthy`), not a
record of these endpoints actually existing and being exercised in the
fork. Do not read "Sprint closed / cards done" as "feature shipped in
this repo" — the Pulse tracking and the repo's real state have
diverged. Writing the actual migration + endpoint code against `app/`
is the next concrete step, separate from and after this doc.

## Pending — 0.3.1 evidence requirements (not yet in effect)

As of 2026-08-11, this board's `impact_evidence_mode` setting reads
`"off"` (confirmed via `okto_pulse_get_board`), and
`okto_pulse_move_card`'s `impact_evidence` block is optional, not
required, in the current tool schema. `okto_pulse_submit_task_validation`
has no evidence-specific parameters. In other words: **structured,
mandatory evidence-on-completion is not live on this board today**,
even though the installed package version (`okto-pulse` /
`okto-pulse-core` 0.3.1) matches the `main`-branch release documented
in `CLAUDE.md`.

Once a build ships that turns evidence-on-completion into a
required, structured gate (e.g. `impact_evidence_mode` defaulting to
`require`, or `submit_task_validation`/`move_card` gaining required
evidence fields), any card completed on this board going forward should
populate that block with real file paths, real test output, and real
diffs — the same standard already used for this spec's test-scenario
evidence — not placeholder content. This section will be updated (and
this caveat removed) once that's confirmed live, not assumed in
advance.
