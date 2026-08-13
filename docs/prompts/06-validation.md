# 6. Validation (Validator)

Give this to your **Validator** agent after the Builder submits a task.
Repeat per task — implementation and test tasks alike.

---

Review the submitted task independently. Load the full spec context,
including any Decisions the Builder may not have referenced. Assess:

- **Confidence** — does the Builder's own account of what it built hold up?
- **Completeness** — does the change satisfy the task's full requirements
  and acceptance criteria, not just part of them?
- **Drift** — does it match what the spec actually asked for, including the
  existing conventions in `docs/decisions/0001-token-auth-scheme.md`?

If all three hold up, approve the task and move it to `done`. If any one
falls short, send it back with a specific reason — not a generic rejection —
so the Builder knows exactly what to fix before resubmitting.

---

**Next:** once a task is approved, the Builder can start any task that
depended on it — see the dependency table in [Sprint & tasks](04-sprint.md).
