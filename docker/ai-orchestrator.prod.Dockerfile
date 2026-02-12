# Production Dockerfile - Slim image with only runtime packages
# Multi-stage build: build wheels first, then create slim runtime image
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /build

# Copy only what's needed to build
COPY pyproject.toml uv.lock README.md ./
COPY packages/ packages/
COPY src/ src/

# Build all packages as wheels
RUN uv build --all-packages --wheel

# Runtime stage - minimal Python image with uv
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app

# Copy built wheels
COPY --from=builder /build/dist /app/dist

# Create venv and install only the built packages (no source code or tooling)
RUN uv venv && \
    uv pip install dist/*.whl && \
    rm -rf /app/dist /root/.cache

# Run as non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Default command runs the orchestrator via uv run (activates venv automatically)
CMD ["uv", "run", "ai-orchestrator"]
