---
name: grill-okf
description: Interview the user relentlessly about a plan, design, or domain, then write resolved decisions and glossary terms as OKF concept files under docs/app/. Use when the user wants to stress-test a plan, pin down domain language, or record design decisions in the project's OKF knowledge base.
---

# /grill-okf

Run a relentless interview about a plan, design, or domain problem. Capture resolved decisions as OKF concept files under `docs/app/decisions/` and glossary terms under `docs/app/concepts/`.

## Quick start

1. Ask the user what they want to grill: a feature, a design, a domain model, or a current problem.
2. Interview them one question at a time. Probe edge cases, dependencies, and terminology.
3. Each time a decision or term resolves, write it as an OKF concept file and update `docs/app/index.md` and `docs/app/log.md`.

## Concept templates

A decision file (`docs/app/decisions/<slug>.md`):

```markdown
---
type: Decision
title: <Short decision title>
description: <One-line summary of the decision>
timestamp: <ISO 8601>
---

# Context

What forced the decision.

# Decision

What we decided.

# Consequences

What this makes easier, harder, or impossible.
```

A glossary term (`docs/app/concepts/<slug>.md`):

```markdown
---
type: Concept
title: <Canonical term>
description: <One-line definition>
timestamp: <ISO 8601>
---

# Definition

Precise meaning in this project.

# Examples

Concrete examples of correct and incorrect usage.

# Related

Links to related concepts and decisions.
```

## Rules

- Ask one question at a time. Wait for an answer before the next question.
- When the user uses vague or overloaded terms, propose a precise canonical term and write it to `docs/app/concepts/`.
- When a trade-off resolves, write it to `docs/app/decisions/`.
- Update `docs/app/index.md` after adding new concepts or decisions.
- Append a one-line entry to `docs/app/log.md` under today's date for every concept created or meaningfully changed.
- Do not create concepts or decisions before the user agrees on the content.
- Bundle-relative links inside OKF should start from `docs/app/` (e.g., `/decisions/0001-use-postgres.md`).
