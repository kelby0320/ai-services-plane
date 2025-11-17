# AI Services Plane

The **AI Services Plane** provides the core AI capabilities of the platform, including:
- LLM text generation
- Embeddings
- Knowledge-base (RAG) indexing and retrieval
- History-augmented generation
- Tool calling (e.g., web search)
- Future multi-model orchestration

This project is designed as a uv workspace and includes the following packages:

* ai-orchestrator - FastAPI service
* ai-core - Core domain functionality
* ai-infra - Infrastructure adapters

## Getting Started

### Prerequisites
* uv

## Running the API

From the repository root:
```bash
uv run ai-orchestrator
```

## Running tests:
```bash
uv run pytest
```
