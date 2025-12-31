#!/bin/bash

set -e

mkdir -p packages/ai-orchestrator/src/ai_orchestrator/grpc/generated

uv run python -m grpc_tools.protoc -I./proto --python_out=packages/ai-orchestrator/src/ai_orchestrator/grpc/generated --grpc_python_out=packages/ai-orchestrator/src/ai_orchestrator/grpc/generated --mypy_out=packages/ai-orchestrator/src/ai_orchestrator/grpc/generated --mypy_grpc_out=packages/ai-orchestrator/src/ai_orchestrator/grpc/generated proto/aisp/v1/chat_orchestrator.proto
