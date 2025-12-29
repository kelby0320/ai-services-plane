## Goal
(What changes from a user / API / behavior perspective?)

---

## Scope (Allowed Changes)
(List specific modules or directories when possible. Prefer the narrowest scope.)

- packages/ai-core/...
- packages/ai-infra/...
- packages/ai-orchestrator/...

---

## Non-Scope (Must NOT Change)
- No changes to:
  - packages/ai-core/<x>
  - existing public APIs
  - unrelated adapters
  - dependency directions

---

## Architectural Constraints
- Follow AGENTS.md strictly
- ai-core must remain infrastructure-agnostic
- Infrastructure adapters live in ai-infra
- Public API concerns live in ai-orchestrator only

---

## Interfaces / Contracts
(Define or reference expected function signatures, Protocols, DTOs.)

Example:
```python
class ModelProvider(Protocol):
    async def generate(self, request: GenerationRequest) -> GenerationResult: ...
```

---

## Data Flow
(Briefly describe how data moves across layers.)

Example:
HTTP → DTO → domain service → port → adapter → result → DTO

---

## Tests

* Unit tests:
  * location:
  * behavior:
* Integration tests (if applicable):

---

## Acceptance Checklist
- [ ] Ruff format passes
- [ ] Ruff check passes
- [ ] Mypy passes
- [ ] Pytest passes
- [ ] No layer boundary violations
- [ ] No unnecessary refactors

---

## Instructions to Agent
* Plan first and present the plan before coding
* Ask before touching files outside scope
* Optimize for minimal, correct changes
* Stop and ask if the requested change appears to violate AGENTS.md