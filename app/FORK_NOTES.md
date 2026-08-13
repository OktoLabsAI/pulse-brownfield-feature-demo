# Fork notes

**Upstream:** https://github.com/nsidnev/fastapi-realworld-example-app
**Forked commit:** `029eb7781c60d5f563ee8990a0cbfb79b244538c` ("Bump asyncpg from
0.25.0 to 0.26.0 (#302)", 2022-08-21). This is the tip of the upstream default
branch at fork time. Upstream has been archived/unmaintained since that
period ("this repository is not actively maintained" per its README).

Cloned as a fresh git history and committed directly into this repo (not a
submodule), per the plan.

## Environment

- No Docker available in this environment, so the app's own `docker-compose.yml`
  / `Dockerfile` path could not be exercised directly. Fell back to the other
  path documented in the upstream README: local PostgreSQL + Poetry.
- PostgreSQL 15 via Homebrew (`brew install postgresql@15`), started with
  `brew services start postgresql@15`. Created role `postgres`/`postgres` and
  database `rwdb` locally (matches the `DATABASE_URL` pattern the upstream
  README uses).
- Poetry 2.2.1 installed via `pip install --user poetry` (upstream pins
  `poetry==1.1` in its Dockerfile, but 2.x installed the pinned
  `poetry.lock`/`pyproject.toml` without complaint — the lockfile format
  round-tripped cleanly, just printed a deprecation notice about
  `poetry.dev-dependencies` vs the newer `poetry.group.dev.dependencies`
  syntax; no action needed).
- Python 3.9.6 (system/Xcode-bundled) used for the virtualenv — satisfies the
  `python = "^3.9"` constraint in `pyproject.toml`.
- `poetry install --no-root` installed the full dependency set
  (`poetry.lock` unmodified) without version conflicts.

## What actually broke, and the fix

**`ModuleNotFoundError: No module named 'pkg_resources'` on `uvicorn`
startup**, raised from `aiosql/__init__.py:4` (`import pkg_resources as pkg`).

- Root cause: `aiosql` (pinned `^6.2`) imports `pkg_resources`, which used to
  ship automatically inside every virtualenv as part of `setuptools`. Modern
  `setuptools` (>=81, released 2025) dropped the bundled `pkg_resources`
  module, and the Poetry-created venv in this environment did not have
  `setuptools` pre-seeded at all — so the import failed outright. This is
  exactly the kind of dependency rot expected from a project unmaintained
  since 2022: it silently depended on packaging-ecosystem behavior that
  changed underneath it.
- Fix: `poetry run pip install "setuptools<81"` into the project's virtualenv.
  This is a dev-environment workaround, not a `pyproject.toml`/lockfile
  change — upstream doesn't declare `setuptools` as a direct dependency at
  all, so the "real" fix (out of scope for a demo fork) would be for `aiosql`
  to stop relying on `pkg_resources`, or for this app to pin `setuptools<81`
  explicitly as a transitive dependency.
- `pkg_resources` also emits a `DeprecationWarning` on every import at
  runtime ("slated for removal as early as 2025-11-30") — cosmetic, left
  as-is.

No other code changes were required. `alembic upgrade head` and
`uvicorn --host=0.0.0.0 app.main:app` both ran clean after the `setuptools`
pin, against the locally running Postgres instance.

## Verification performed

With the server running on `:8000`:

- `POST /api/users` (register) → `200`, returns `{"user": {..., "token": "<jwt>"}}`.
- `POST /api/users` again with the same username → `400`,
  `{"errors": ["user with this username already exists"]}`.
- `POST /api/users` with an empty body → `422`,
  `{"errors": [{"loc": [...], "msg": "field required", "type": "value_error.missing"}, ...]}`.
- `GET /api/user` with no `Authorization` header → `403`,
  `{"errors": ["authentication required"]}`.
- `GET /api/user` with `Authorization: Token <jwt>` → `200`, returns the user.
- `GET /api/user` with `Authorization: Bearer <jwt>` → `403`,
  `{"errors": ["unsupported authorization type"]}`.

See `docs/decisions/0001-token-auth-scheme.md` for what these confirm about
the auth scheme and error-response shape.
