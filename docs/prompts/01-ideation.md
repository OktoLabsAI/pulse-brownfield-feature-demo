# 1. Ideation

Give this to your agent to open the ideation on the `pulse-brownfield-feature-demo` board.

---

Read `app/FORK_NOTES.md` and the existing comment-handling code in this fork
(`app/db/repositories/commentaries.py`, the `commentaries` table, and the
comment routes under `app/api/routes/`) to understand how article comments
work today.

Today a comment belongs only to an article and an author — there's no
reply-to relationship and no way to tag another user inside a comment body.

Open an Ideation on the `pulse-brownfield-feature-demo` board for a feature
that adds:

1. **Threaded replies** — replying to a specific existing comment so a
   conversation reads as a thread instead of a flat, unordered list.
2. **@mentions** — tagging another registered user by username inside a
   comment body so they can be made aware they were referenced.

State the problem in terms of what today's flat comment list can't do, and
propose extending the existing `commentaries` domain rather than introducing
a new entity, so the approach stays consistent with the rest of the RealWorld
data model.

---

**Next:** once the ideation is recorded, move to [Refinement](02-refinement.md).
