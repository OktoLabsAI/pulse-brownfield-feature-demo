# 7. Testing (Builder)

Give one of these to your **Builder** agent per test task, once its matching
implementation task is `done`. Send each to [Validation](06-validation.md)
after submitting.

---

## Test: reply threading

Implement and actually run the reply-threading test scenario against the
running app: creating a reply, enforcing the one-level depth limit, and
confirming a reply can't target a comment on a different article. Only
record the result as passed once you've verified it executed successfully —
writing the test isn't sufficient on its own.

## Test: @mentions

Implement and actually run the @mentions test scenario: mention resolution
against registered usernames, and listing a comment's resolved mentions.
Only record the result as passed once verified.

## Test: cascade delete of replies

Implement and actually run the cascade-delete test scenario: deleting a
top-level comment removes its replies too. Only record the result as passed
once verified.

---

**Next:** once every implementation and test task is approved, move to
[Close-out](08-close-out.md).
