# 5. Implementation (Builder)

Give one of these to your **Builder** agent per task, in dependency order.
After each submission, send the matching task to [Validation](06-validation.md)
before starting the next one.

---

## Migration task

Pull this task's requirements and linked spec context from the board, then
implement the migration against `app/`: a nullable, self-referential
`parent_comment_id` column on `commentaries` (same-article FK), and a new
`comment_mentions` table (`comment_id`, `mentioned_user_id`). Write the
Alembic migration, run it, and confirm the schema change against the running
database. Move the task through its lifecycle and submit it for review with
a summary of what changed, a completeness estimate, and any deviation from
spec.

## Reply threading task

Pull this task's requirements and linked spec context. Implement reply
creation (a comment with a non-null `parent_comment_id`) and its validation
rules: replies limited to one level deep, and a reply must target a
top-level comment on the same article. Extend the read path so replies are
returned nested under their parent. Submit for review with a completeness
estimate and any noted deviation from spec.

## @mentions task

Pull this task's requirements and linked spec context. Implement @mention
parsing on comment write (extract `@username` tokens, resolve against
existing registered usernames, persist into `comment_mentions`) and the read
path for listing a comment's resolved mentions. Submit for review with a
completeness estimate and any noted deviation from spec.

---

**Next:** [Validation](06-validation.md) for each task above, then
[Testing](07-testing.md) once threading and mentions are both approved.
