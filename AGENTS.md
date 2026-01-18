# AGENTS.md — AI Services Plane (AISP)

This file defines NON-NEGOTIABLE rules for AI agents working in the
AI Services Plane (AISP) repository.

AISP uses a layered, ports-and-adapters architecture.
Violating architectural boundaries is a correctness failure,
even if the code runs or tests pass.

---

## Repository Structure

```
ai-services-plane/
└── packages/
    ├── ai-core/
    ├── ai-infra/
    └── ai-orchestrator/
```

This structure is intentional and must be preserved.

---

## Architectural Layers

### ai-core (Domain Layer)

The ai-core package contains PURE business logic.

Allowed contents:
- domain models
- domain services
- domain errors
- ports (Protocols)

Hard constraints:
- MUST NOT depend on ai-infra
- MUST NOT depend on ai-orchestrator
- MUST NOT reference:
  - HTTP or gRPC
  - databases
  - external services or SDKs
  - environment variables or config loading
- MUST NOT contain serialization or transport logic

All logic here must be framework-agnostic and testable in isolation.

---

### ai-infra (Infrastructure Layer)

The ai-infra package contains implementations of domain ports.

Responsibilities:
- database access
- model providers
- external APIs
- file systems, queues, caches
- adapters for LLM providers

Constraints:
- MAY depend on ai-core
- MUST NOT depend on ai-orchestrator
- MUST NOT contain business logic
- MUST NOT define public API schemas

---

### ai-orchestrator (API / Boundary Layer)

The ai-orchestrator package coordinates execution and exposes servers.

Responsibilities:
- HTTP and gRPC server implementations
- request/response DTOs
- serialization and validation
- dependency injection and wiring
- coordination of ai-core via ai-infra

Constraints:
- MAY depend on ai-core
- MAY depend on ai-infra
- MUST NOT contain business logic

---

## Dependency Rules (Hard Constraints)

These rules are strictly enforced:

- ai-core
  - MUST NOT import ai-infra
  - MUST NOT import ai-orchestrator

- ai-infra
  - MAY import ai-core
  - MUST NOT import ai-orchestrator

- ai-orchestrator
  - MAY import ai-core
  - MAY import ai-infra

Breaking dependency direction is a correctness failure.
If a change requires violating these rules, the agent MUST STOP and ask.

---

## Ports and Adapters

- Ports (Protocols) are defined in ai-core
- Adapters implementing ports live in ai-infra
- ai-core must never know which adapter is used
- Dependency injection occurs in ai-orchestrator (or infra initialization)

---

## Tooling Rules (Strict)

This repository uses uv for all tooling.
Agents MUST use uv correctly.

### Formatting and Linting
```sh
uv run ruff format
uv run ruff check
```

### Type Checking
```sh
uv run mypy .
```

### Tests
```sh
uv run pytest
```

All new code MUST be typed.
Mypy errors are treated as failures.

---

## Dependency Management (Critical Rule)

- MUST NOT manually edit pyproject.toml to add dependencies
- MUST use uv commands to manage dependencies

Required usage:
```sh
uv add <package>
uv add <package> --extra <extra>
uv add <package> --dev
```

Rationale:
- Manual edits frequently introduce incorrect or incompatible versions
- uv is the authority on dependency resolution

Manual dependency edits are considered a tooling violation.

---

## Coding Conventions

- Use explicit classes and types
- Prefer Protocols and dataclasses to dicts
- Avoid implicit or duck-typed interfaces
- Keep functions and classes small and focused
- Avoid magic constants; use named values
- Do not introduce architectural coupling for convenience

---

## Agent Workflow (Required)

Agents must follow this workflow:

1. **Plan first**
   - Identify files and packages to change
   - Describe data flow across layers
   - Identify ports and adapters involved

2. **Stop AND ask** before proceeding if the plan:
   - adds dependencies
   - introduces new packages
   - changes public APIs or gRPC schemas
   - crosses layer boundaries unexpectedly

3. **Implement with minimal diff**
   - Change only what the work order requires
   - Avoid unrelated refactors
   - Do not move code across layers without instruction

4. **Verify**
   - Run formatting, linting, typing, and tests
   - Re-check dependency direction

---

## Mandatory Stop Conditions

Agents MUST STOP and report if:

- a change violates dependency rules
- business logic appears outside ai-core
- a new port or adapter is required but unclear
- scope expands beyond the assigned work order

Guessing is worse than asking.

---

## Guiding Principle

> Correct architecture outweighs speed.
> Small, correct changes are preferred over large refactors.