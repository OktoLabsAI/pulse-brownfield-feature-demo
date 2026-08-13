# 4. Sprint & tasks

Give this to your agent once the spec is `approved`, to open Sprint 1 and
create its tasks.

---

Open "Sprint 1 — Comments Threading + Mentions" against the approved spec,
and create its six tasks with these dependencies:

| Task | Depends on |
| ---- | ---------- |
| Migration: `parent_comment_id` column + `comment_mentions` table | None — start here |
| Implement reply threading (create + validation) | Migration |
| Implement @mention parsing/resolution + read paths | Migration |
| Test: reply threading (create, depth limit, cross-article) | Threading implementation |
| Test: @mentions resolution and listing | Mentions implementation |
| Test: cascade delete of replies | Threading implementation |

Don't start the two implementation tasks (threading, mentions) until the
migration task is `done`. Don't start a test task until its matching
implementation task is `done`.

---

**Next:** work each task through [Implementation](05-implementation.md) and
[Validation](06-validation.md), then [Testing](07-testing.md).
