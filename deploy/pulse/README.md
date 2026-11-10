# One-click Railway deploy (Okto Pulse + MCP)

Runs `okto-pulse` behind a Caddy gateway on a single public port.
Pulse Community has **no login of its own**, so Caddy adds it:

| Path | Protection |
|---|---|
| `/` , `/api/*` (UI + REST) | Basic auth: `UI_USER` / `UI_PASSWORD` |
| `/mcp` | `Authorization: Bearer <MCP_TOKEN>` or `?token=<MCP_TOKEN>` |
| `/healthz` | open, returns `ok` |

## Create the Railway template (once)
1. Railway → Workspace → Templates → **New Template**.
2. Add a service from this GitHub repo. Settings:
   - Variable `RAILWAY_DOCKERFILE_PATH` = `deploy/pulse/Dockerfile`
   - Enable public networking (HTTP). Healthcheck path `/healthz`.
   - Right-click service → **Attach Volume**, mount path `/data`.
3. Variables (Variables tab):
   - `UI_USER` = `demo`
   - `UI_PASSWORD` = `${{secret(24)}}`
   - `MCP_TOKEN` = `${{secret(32)}}`
4. **Create Template**, copy the URL, then add this button to the README:
   `[![Deploy on Railway](https://railway.com/button.svg)](<template-url>)`

## After a visitor deploys
1. Open the generated domain and log in with `UI_USER` / `UI_PASSWORD` (shown in the service Variables tab).
2. Create an agent in the UI and copy its key (it starts with `dash_` and is shown once). The seeded agents only hold hashed keys.
3. Connect the agent. The gateway token and the agent key are both required:
   `claude mcp add --transport http pulse "https://<domain>/mcp?api_key=<agent-key>" --header "Authorization: Bearer <MCP_TOKEN>"`
   Clients that only take a URL can use `https://<domain>/mcp?token=<MCP_TOKEN>&api_key=<agent-key>`.

## Local test
`docker build -f deploy/pulse/Dockerfile -t pulse . && docker run -p 8080:8080 -e PORT=8080 -e UI_PASSWORD=pw -e MCP_TOKEN=tok -v pulse-data:/data pulse`

## Seed board
`seed/pulse.db` is a **repaired copy** of `data/pulse.db` (the original is untouched). The original cannot be loaded: Pulse 0.3.0-0.4.2 abort on it.
Repairs, all on the copy, tested by booting Pulse 0.3.3 and reading the board back through the API:
- Removed 720 foreign-key orphans (270 `quality_finding_qa_links`, 270 `quality_proposed_questions`, 56 `quality_assessment_outbox`, 1 import resolution, 123 of 176 `kuzu_node_refs` knowledge-graph refs).
- Set one `guideline_impact_receipts.item_count` from 9 to 3 (only 3 item rows exist in the source).
- Cleared the `quality_assessment_legacy_import_*` bookkeeping tables (a digest check failed on them).
Ideation, refinement, spec, card and finding rows are unchanged (counts match the original). Delete-guard triggers were dropped for the cleanup and recreated.
The seed is copied to the volume on first boot only. It also holds the board's agent records, so keep the deploy password-gated.

Pinned: `okto-pulse==0.3.3` + `okto-pulse-core==0.3.3` (0.3.3 only requires `okto-pulse-core>=0.3.3`, so an unpinned install pulls an incompatible core; 0.4.x pins its core). Image about 2.2 GB (CPU-only torch).

## Checked and not checked
Checked locally with Docker: the image builds (about 5 min); the UI is behind basic auth; `/mcp` rejects a missing or wrong token; the seeded board is readable through the API; an agent created in the UI can call MCP tools with the token plus its key (query form and header form); three restarts keep data, and the seed is not applied again; recovery after a hard kill takes about 40 s. Not checked on Railway itself.
