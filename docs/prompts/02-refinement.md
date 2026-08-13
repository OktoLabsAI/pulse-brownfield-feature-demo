# 2. Refinement

Give this to your agent once the Ideation exists, to turn it into a concrete
data model and API shape.

---

Refine the "Threaded Replies + @Mentions for Article Comments" ideation into
a concrete data model and API contract:

1. **Threading** — add a nullable, self-referential `parent_comment_id`
   (foreign key to `commentaries.id`, same article) to the comment record.
   `parent_comment_id = null` means top-level; non-null means it's a reply.
   Limit depth to one level — replies to top-level comments only, no
   reply-to-reply nesting.
2. **@Mentions** — parse the comment body for `@username` tokens at write
   time, resolve each against existing registered usernames (case-sensitive
   exact match, consistent with how usernames are looked up elsewhere in the
   fork), and persist resolved mentions as first-class records
   (`comment_id`, `mentioned_user_id`) rather than leaving them as
   unstructured text in the body.

Before finalizing the shape, check `docs/decisions/0001-token-auth-scheme.md`
so any new/changed endpoints stay consistent with the fork's existing auth
scheme (`Authorization: Token <jwt>`) and flat `{"errors": [...]}` error
contract — don't assume a different shape.

---

**Next:** once refinement is recorded, move to [Spec](03-spec.md).
