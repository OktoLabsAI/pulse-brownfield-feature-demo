# 0001 — Use the `Authorization: Token <jwt>` scheme (not `Bearer`), and a flat `{"errors": [...]}` error shape (not nested by field)

- **Status:** Accepted
- **Date:** 2026-08-10
- **Scope:** `app/` (forked from
  [`nsidnev/fastapi-realworld-example-app`](https://github.com/nsidnev/fastapi-realworld-example-app)
  @ `029eb7781c60d5f563ee8990a0cbfb79b244538c`)

## Context

Before building the threaded-replies + @mentions feature on top of this fork,
we need to know — from the actual running code, not assumption — what auth
scheme and error-response contract the rest of the app already follows, so
new endpoints stay consistent.

This is a fork of a reference implementation of the
[RealWorld / "Conduit" API spec](https://github.com/gothinkster/realworld):
the app's own README states its purpose is "passing Conduit testsuite," and
the FastAPI OpenAPI errors module is customized specifically to match that
spec's expected shape (see `validation_error.py` below). The Token scheme and
custom error envelope are therefore not incidental choices by this fork's
author — they're conformance requirements of the spec that this whole
codebase exists to implement.

## Decision

### 1. Auth scheme is literally `Token`, not `Bearer`

`app/core/settings/app.py:29`:

```python
jwt_token_prefix: str = "Token"
```

Enforced in `app/api/dependencies/authentication.py:46-63`
(`_get_authorization_header`):

```python
def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
    settings: AppSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token
```

`strings.WRONG_TOKEN_PREFIX` (`app/resources/strings.py:17`) is
`"unsupported authorization type"`.

Confirmed empirically against a running instance (see
`app/FORK_NOTES.md`):

```
$ curl http://localhost:8000/api/user -H "Authorization: Token <jwt>"
200  {"user": {...}}

$ curl http://localhost:8000/api/user -H "Authorization: Bearer <jwt>"
403  {"errors": ["unsupported authorization type"]}
```

`Bearer` is not a fallback or an alias — it is explicitly rejected. Nothing
in the diff between fork commit and HEAD suggests this was ever `Bearer` and
changed; it's the scheme mandated by the Conduit/RealWorld spec, which
several other language implementations of the same spec also follow (so this
isn't a quirk of this one Python port — the app is conforming to an external
contract).

### 2. Error shape is a flat `{"errors": [...]}` list — **not** `{"errors": {"field": ["msg"]}}`

Two handlers register the same top-level key but with different item shapes,
both registered in `app/main.py:37-38`:

`app/api/errors/http_error.py` (business/auth errors, e.g. 400/403):

```python
async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
```

`app/api/errors/validation_error.py` (422 request-validation errors):

```python
async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )
```

Confirmed empirically:

```
$ curl -X POST /api/users -d '{"user":{"username":"testuser",...}}'  # dup
400  {"errors": ["user with this username already exists"]}

$ curl -X POST /api/users -d '{"user":{}}'
422  {"errors": [
  {"loc": ["body","user","email"], "msg": "field required", "type": "value_error.missing"},
  {"loc": ["body","user","password"], "msg": "field required", "type": "value_error.missing"},
  {"loc": ["body","user","username"], "msg": "field required", "type": "value_error.missing"}
]}

$ curl /api/user   # no Authorization header
403  {"errors": ["authentication required"]}
```

**This is a correction to the assumed contract, not a confirmation of it.**
The originally assumed shape (`{"errors": {"field": ["msg"]}}`, matching the
canonical RealWorld/Conduit spec doc) is **not** what this fork actually
implements. `errors` is always a JSON **array** here:
- an array of plain strings for business/auth errors (`http_error_handler`),
- an array of pydantic's raw `{loc, msg, type}` validation-error objects for
  422s (`http422_error_handler`) — not even grouped by field name, just a
  flat list in validation order.

Any new endpoint we add (threaded replies, @mentions) must raise
`fastapi.HTTPException` for business errors and let pydantic/FastAPI's
built-in validation produce 422s, so it free-rides on these two existing
handlers rather than inventing a third response shape.

## Alternatives considered

No alternative was implemented in this codebase — there is exactly one auth
scheme and one pair of error handlers, registered globally in `main.py`, with
no per-route overrides found anywhere in `app/api/routes/`. We looked for
evidence of deliberate choice vs. accident:

- The `RWAPIKeyHeader` wrapper class (`authentication.py:21-32`) exists
  specifically to intercept Starlette's default `APIKeyHeader` 403 and
  re-raise it through the app's own `strings.AUTHENTICATION_REQUIRED` /
  `http_error_handler` path, so even the "missing header entirely" case comes
  back in the same `{"errors": [...]}` envelope instead of FastAPI's default
  security-scheme error shape. That's deliberate effort to keep one
  consistent contract, not an oversight.
- `validation_error.py:22-28` goes further and monkey-patches FastAPI's
  OpenAPI schema (`validation_error_response_definition["properties"]`) so
  the *generated docs* also describe `errors` as an array — i.e., the author
  treated the array shape as the documented public contract, not an
  implementation accident.
- No `Bearer` handling exists anywhere (no dead code, no comment referencing
  it), and the spec badges in `README.rst` point at the Conduit/RealWorld
  testsuite this app is built to pass — which is what fixes `Token` as the
  scheme in the first place, upstream of this fork's own choices.

## Consequences

- New auth-protected routes for threaded replies / @mentions must depend on
  `get_current_user_authorizer()` (or `..._optional()`) from
  `app/api/dependencies/authentication.py`, unchanged — no new auth
  mechanism.
- New business-rule failures (e.g. "cannot reply to a deleted thread",
  "mentioned user does not exist") should be raised as
  `HTTPException(status_code=..., detail="<message>")` so they render as
  `{"errors": ["<message>"]}`, consistent with existing routes.
- Anything downstream (spec, ideation, or test-scenario write-ups) that
  assumed the nested `{"errors": {"field": [...]}}` shape needs to be
  corrected to the flat-array shape documented here before it's treated as
  ground truth.
