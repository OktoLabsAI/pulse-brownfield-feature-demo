# One-click Railway image: Okto Pulse (UI + MCP) behind a Caddy auth gateway.
# Build context = repo root. On Railway set RAILWAY_DOCKERFILE_PATH=deploy/pulse/Dockerfile
FROM caddy:2 AS caddy

FROM python:3.12-slim
ARG OKTO_PULSE_VERSION=0.3.3
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_DEFAULT_TIMEOUT=120 PIP_RETRIES=10 \
    HF_HOME=/opt/hf-cache SENTENCE_TRANSFORMERS_HOME=/opt/hf-cache/sentence_transformers \
    DATA_DIR=/data KG_BASE_DIR=/data \
    HOST=127.0.0.1 MCP_HOST=127.0.0.1 OKTO_PULSE_NO_BANNER=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=caddy /usr/bin/caddy /usr/local/bin/caddy
# CPU-only torch keeps the image ~3 GB smaller than the default CUDA wheel.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
# okto-pulse does not pin its core, so pin both or pip may pick an incompatible core.
RUN pip install "okto-pulse==${OKTO_PULSE_VERSION}" "okto-pulse-core==${OKTO_PULSE_VERSION}"
# Bake the embedding model so first boot works offline.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
WORKDIR /app
COPY deploy/pulse/Caddyfile deploy/pulse/entrypoint.sh /app/
# Optional seed: put a Pulse-compatible pulse.db in deploy/pulse/seed/. Copied to the volume on first boot only.
COPY deploy/pulse/seed/ /seed/
RUN chmod +x /app/entrypoint.sh
EXPOSE 8080
CMD ["/app/entrypoint.sh"]
