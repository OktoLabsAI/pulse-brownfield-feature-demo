# 3. Spec

Give this to your agent once Refinement exists, to turn it into an
implementable spec — and to get it approved.

---

Turn the "Comments Threading + Mentions" refinement into a full spec:

- **Technical requirements**: the `parent_comment_id` migration, the new
  `comment_mentions` table, the reply-threading create/read logic, and the
  @mention parsing/resolution logic.
- **API contracts**: how `POST`/`GET /api/articles/{slug}/comments` change to
  support replies and mentions, following the existing fork's request/response
  conventions (`docs/decisions/0001-token-auth-scheme.md`).
- **Acceptance criteria**: what "done" means for threading (create, depth
  limit, cross-article isolation, cascade delete of replies) and for mentions
  (resolution correctness, listing).

Once the spec content is complete, submit it for approval so a sprint can be
opened against it. A sprint cannot be created until the spec reaches
`approved`.

---

**Next:** once the spec is approved, move to [Sprint & tasks](04-sprint.md).
