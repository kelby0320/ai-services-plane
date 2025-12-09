FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder
WORKDIR /usr/src/ai_services_plane
COPY . .
RUN uv venv
RUN uv build --all-packages --wheel
RUN uv pip install dist/*.whl
CMD ["uv", "run", "ai-orchestrator"]
