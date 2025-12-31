This file defines the rules, constraints, and expected behavior for AI agents
working in this repository. All automated coding agents (Cursor, Copilot, etc.)
must follow these instructions.

This repository uses a **layered, ports-and-adapters architecture**.
Violating architectural boundaries is considered a correctness bug.

---

## Repository Structure

```
ai-services-plane/
└── packages/
    ├── ai-core/
    ├── ai-infra/
    └── ai-orchestrator/
```

---

## Architectural Overview

### ai-core (Domain Layer)
- Contains **business logic only**
- Defines **domain models, services, and ports (Protocols)**
- **Must not depend on** ai-infra or ai-orchestrator
- Must not reference infrastructure concerns:
  - HTTP, gRPC
  - databases
  - external services
  - environment/config loading
- Uses explicit types and interfaces

### ai-infra (Infrastructure Layer)
- Depends on ai-core
- Implements ports (Protocols) defined in ai-core
- Contains adapters for:
  - databases
  - model providers
  - external APIs
  - file systems, queues, caches, etc.
- Must not contain business logic
- Must not define public API schemas

### ai-orchestrator (API / Boundary Layer)
- Depends on ai-core and ai-infra
- Contains HTTP and gRPC server implementations
- Owns:
  - request/response DTOs
  - serialization
  - transport-level validation
- Coordinates calls into ai-core via ai-infra
- Must not contain business logic

---

## Dependency Rules (Hard Constraints)

The following rules are **non-negotiable**:

- ai-core:
  - ❌ must not import ai-infra
  - ❌ must not import ai-orchestrator

- ai-infra:
  - ✅ may import ai-core
  - ❌ must not import ai-orchestrator

- ai-orchestrator:
  - ✅ may import ai-core
  - ✅ may import ai-infra

If a change requires breaking these rules, the agent **must stop and ask**.

---

## Ports & Adapters Pattern

- Ports (Protocols) are defined in ai-core
- Adapters implementing those ports live in ai-infra
- ai-core must never know which adapter is used
- Dependency injection is performed in ai-orchestrator or ai-infra

---

## Tooling & Quality Gates

Agents must ensure the following pass before considering work complete:

- Formatting & linting:
  - uv run ruff format
  - uv run ruff check
- Type checking:
  - uv run mypy .
- Tests:
  - uv run pytest

All new code **must** be typed. Mypy errors are treated as failures.

---

## Coding Conventions

- Use explicit classes and types
- Prefer Protocols and dataclasses to dicts
- Avoid implicit or duck-typed interfaces
- Keep functions and classes small and focused
- No magic constants; use named values
- Do not introduce architectural coupling for convenience

---

## Agent Workflow (Required)

Agents must follow this workflow:

1. **Plan first**
   - List files/modules to change
   - Describe data flow across layers
   - Identify which ports/adapters are involved

2. **Wait for approval** if the plan:
   - touches new packages
   - adds dependencies
   - changes public APIs
   - crosses layer boundaries

3. **Implement with minimal diff**
   - Avoid refactors unrelated to the task
   - Do not move code across layers unless explicitly requested

4. **Verify**
   - Run formatting, linting, typing, and tests
   - Re-check dependency direction

---

## When to Stop and Ask

Agents must stop and ask for clarification if:

- A required change violates dependency rules
- Business logic appears to belong in a different layer
- A new port or adapter is required but unclear
- Scope expands beyond the original work order

Silence or guessing is worse than asking.

---

## Guiding Principle

> Correct architecture is more important than speed.
> Small, composable changes are preferred over large refactors.