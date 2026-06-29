---
name: refer-okf
description: Query the OKF knowledge bundle under docs/app/ to answer questions and provide grounded context. Use when the user asks about project terms, design decisions, systems, datasets, or any fact recorded in OKF.
---

# /refer-okf

Answer questions using only the OKF knowledge bundle under `docs/app/`. Read `docs/app/index.md`, follow relevant cross-links, and synthesize a grounded response.

## Quick start

1. Read `docs/app/index.md` to find the concept directories and any directory indexes.
2. Identify which concepts are relevant to the user's question.
3. Read those concept files.
4. Follow cross-links (`/concepts/...`, `/decisions/...`, `/systems/...`) until you have enough context.
5. Answer the question, citing the concept files you used.

## Query patterns

- **Term definition** — read `docs/app/concepts/<term>.md` or search the `concepts/` directory.
- **Design decision** — read `docs/app/decisions/<slug>.md`.
- **System overview** — read `docs/app/systems/<slug>.md`.
- **Data asset** — read `docs/app/datasets/<slug>.md`, `docs/app/tables/<slug>.md`, or `docs/app/pipelines/<slug>.md`.
- **Open-ended** — scan `docs/app/index.md` and the most relevant directory indexes, then read the top matches.

## Rules

- Always start from `docs/app/index.md`.
- Prefer bundle-relative links found in OKF documents over guessing paths.
- When an answer depends on a design decision, cite the decision file.
- When an answer depends on a glossary term, cite the concept file.
- If the OKF bundle does not contain the answer, say so clearly and suggest which concept or decision might need to be created.
- Do not hallucinate outside the OKF bundle. Ground every claim in a file under `docs/app/`.
