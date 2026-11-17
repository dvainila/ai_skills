---
name: prevent-overengineering
description: Enforces YAGNI, KISS, and stops the agent from adding redundant safety/logic layers. Use when writing code, refactoring, adding error handling, or reviewing a patch for overengineering and defensive-programming overkill.
triggers:
  - when: writing code
  - when: refactoring
  - when: adding error handling
---

# Code minimalism and brevity

You tend to over-engineer: you create too many abstraction layers, add redundant protection (try-catch, validators) where the environment or caller is already isolated, and write code "for the future."

**Your main job is to write the smallest amount of code that solves the current task.**

### 1. Architectural principles (KISS + YAGNI)

- **YAGNI (You Aren't Gonna Need It):** Implement only what is requested right now. No future-proofing, abstract factories, or interfaces for a single class.
- **KISS (Keep It Simple, Stupid):** The simplest solution is the right one. If a standard function can solve the task, do not write your own helper.

### 2. Ban on excessive protection (defensive programming overkill)

- **Do not duplicate validation:** If data is already validated at the boundary (for example, by a DTO, middleware, or a database schema), do not repeat those checks inside business logic.
- **Sensible try-catch:** Do not wrap every trivial operation in exception handling. Let exceptions propagate when the application already has a global error handler.
- **Existing context:** Before adding a safety check, study the calling context. Check only what is actually at risk.

### 3. The "Goldilocks zone" and the `/goal-sloc` metric

- Your patch should be at most 1–1.5 times larger than the reference solution. Less code means fewer bugs.
- Before you deliver an answer, self-audit: find at least two places in your code that can be shortened or simplified without losing reliability.
- Ruthlessly delete dead code, redundant comments, and placeholder intermediate variables.
