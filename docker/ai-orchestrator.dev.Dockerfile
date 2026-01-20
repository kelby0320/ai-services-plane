# Development Dockerfile - Large image with codebase and tooling
FROM ghcr.io/astral-sh/uv:python3.14-trixie

WORKDIR /usr/src/ai_services_plane

COPY pyproject.toml uv.lock README.md ./
COPY packages/ packages/
COPY src/ src/

# Create virtual environment and install all packages (including dev dependencies)
RUN uv venv && \
    uv sync --all-packages --dev

# Default command runs the orchestrator
CMD ["uv", "run", "ai-orchestrator"]
