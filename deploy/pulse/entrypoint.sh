#!/bin/sh
set -eu
: "${PORT:=8080}"
: "${UI_USER:=demo}"
: "${UI_PASSWORD:?Set UI_PASSWORD}"
: "${MCP_TOKEN:?Set MCP_TOKEN}"
export PORT UI_USER MCP_TOKEN
export UI_PASSWORD_HASH="$(caddy hash-password --plaintext "$UI_PASSWORD")"

# Seed the persistent volume once.
mkdir -p "$DATA_DIR/data"
if [ -f /seed/pulse.db ] && [ ! -f "$DATA_DIR/data/pulse.db" ]; then
  echo "Seeding $DATA_DIR/data/pulse.db"
  cp /seed/pulse.db "$DATA_DIR/data/pulse.db"
fi

# Pulse reads $PORT as its own API port; Railway injects PORT for the public port, so unset it here.
env -u PORT okto-pulse serve --api-port 8100 --mcp-port 8101 &
PULSE_PID=$!
trap 'kill $PULSE_PID 2>/dev/null; exit 0' TERM INT

# Wait for Pulse before opening the public port
for i in $(seq 1 120); do
  curl -fsS http://127.0.0.1:8100/api/v1/kg/settings >/dev/null 2>&1 && break
  kill -0 $PULSE_PID 2>/dev/null || { echo "Pulse exited"; exit 1; }
  sleep 2
done
exec caddy run --config /app/Caddyfile --adapter caddyfile
