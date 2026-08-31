# Walkthrough: From Clone to Closed Sprint

You've cloned the repo and run the [Quickstart](../README.md#quickstart): Pulse is installed, the demo board is seeded, `okto-pulse serve` is running, and you have two agent identities connected to `pulse-brownfield-feature-demo` — one on the Executor (Builder) preset, one on the Validator preset.

This is what to do from there. Work through the stages below in order, each with a linked prompt file containing what to actually give the agent. Ideation, Refinement, and Spec are already recorded on the seeded board; Sprint and Tasks are what you drive live.

| Stage | What happens | Prompt |
| ----- | ------------ | ------ |
| 1. Ideation | Problem + proposed approach for the feature, grounded in the actual fork code | [`prompts/01-ideation.md`](prompts/01-ideation.md) |
| 2. Refinement | Ideation turned into a concrete data model and API shape | [`prompts/02-refinement.md`](prompts/02-refinement.md) |
| 3. Spec | Refinement turned into an approved, implementable spec | [`prompts/03-spec.md`](prompts/03-spec.md) |
| 4. Sprint & tasks | Spec broken into the sprint's 6 tasks | [`prompts/04-sprint.md`](prompts/04-sprint.md) |
| 5. Implementation | Builder implements each task against `app/` | [`prompts/05-implementation.md`](prompts/05-implementation.md) |
| 6. Validation | Validator reviews each submission independently | [`prompts/06-validation.md`](prompts/06-validation.md) |
| 7. Testing | Builder implements and runs the matching test scenarios | [`prompts/07-testing.md`](prompts/07-testing.md) |
| 8. Close-out | Sprint evaluated and closed, spec marked complete | [`prompts/08-close-out.md`](prompts/08-close-out.md) |

## Before you start

Read these two so both agents are working from the same ground truth, not assumption:

- `app/FORK_NOTES.md` — what this fork is and how it's set up
- `docs/decisions/0001-token-auth-scheme.md` — the auth scheme and error-response shape the fork already uses; any new endpoint has to match it

## Running order

1. **Ideation → Refinement → Spec** happen once, in sequence, on the Spec Writer identity (or your Builder identity if you're not using a separate Spec Writer preset). Each stage only opens once the one before it is in a state that allows it — you can't refine before ideation exists, and a sprint can't open until the spec is `approved`.
2. **Sprint & tasks** — once the spec is approved, open Sprint 1 and create its six tasks (see the [Sprint Stages](../README.md#sprint-stages) table in the README for the full list and their dependencies).
3. **Implementation and validation run task-by-task, not stage-by-stage.** For each task: prompt the Builder to implement it, then prompt the Validator to review it. Don't start a task's dependent tasks until it's approved (e.g. don't start the threading or mentions tasks until the migration task is `done`).
4. **Testing** follows the same pattern once its matching implementation task is approved.
5. **Close-out** only once every task above is `done` and every test has genuinely passed — the Validator submits the sprint evaluation, and the spec is marked complete last.

If a submission comes back from the Validator with changes requested, the Builder fixes it and resubmits — the task doesn't move forward until it's actually approved.
