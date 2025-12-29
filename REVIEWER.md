# Reviewer Instructions — AISP Architecture Review

You are reviewing a proposed or completed change in this repository.

Your task is NOT to rewrite code, but to identify architectural issues.

---

## Review Checklist

### Dependency Direction
- Does ai-core import ai-infra or ai-orchestrator?
- Does ai-infra import ai-orchestrator?
- Are new dependencies justified?

---

### Layer Responsibilities
- Is business logic leaking into ai-infra or ai-orchestrator?
- Are infrastructure details leaking into ai-core?
- Are DTOs confined to ai-orchestrator?

---

### Ports & Adapters
- Are ports defined in ai-core?
- Are adapters implemented in ai-infra?
- Is dependency inversion preserved?

---

### Code Quality
- Are types explicit and complete?
- Are Protocols used appropriately?
- Are error boundaries clear?

---

### Tests
- Are new behaviors tested?
- Are tests placed in the correct layer?
- Are tests too tightly coupled to infra?

---

## Output Format

Provide:
1. **Critical violations** (must fix)
2. **Warnings** (should fix)
3. **Suggestions** (optional improvements)

Be precise. Reference files and symbols.
Do NOT propose refactors beyond scope.