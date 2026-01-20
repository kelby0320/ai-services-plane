set dotenv-load := true

default: build

# ----- Dev commands -----

build:
    uv build

test:
    uv run pytest

fmt:
    uv run ruff format

lint:
    uv run ruff check --fix

run:
    uv run ai-orchestrator

# ----- Database/migrations -----

db-migrate:
    uv run alembic -c packages/ai-infra/alembic.ini upgrade head 

# ----- Docker -----

docker-build: docker-build-dev

docker-build-dev:
    docker build -t ai-orchestrator-dev:latest -f docker/ai-orchestrator.dev.Dockerfile .

docker-build-prod:
    docker build -t ai-orchestrator:latest -f docker/ai-orchestrator.prod.Dockerfile .

# ----- Docker Compose -----

compose-up:
    docker compose up -d

compose-down:
    docker compose down

compose-logs:
    docker compose logs -f