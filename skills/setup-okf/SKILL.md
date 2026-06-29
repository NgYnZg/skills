---
name: setup-okf
description: Initialize a repo with an OKF knowledge base under docs/app/, set up the issue tracker, and run /grill-okf for project initiation. Use when starting a new project or onboarding an existing repo to OKF and agent-ready engineering workflows.
---

# /setup-okf

Set up a repo so it is ready for OKF-backed, agent-assisted work. Creates the OKF bundle under `docs/app/`, configures the issue tracker, writes agent instruction files, and runs `/grill-okf`.

## Before you start

- A git repo is required. If none exists, run `git init` and ask the user to add a remote.
- If no remote exists and the user wants GitHub/GitLab tracking, ask them to create/choose a remote before continuing.

## Process

Run the sections below one at a time. Confirm the user's answer before moving on.

### 1. Explore the repo

Read what already exists:

- `git remote -v`
- `README.md`
- `CONTEXT.md` (if any)
- `docs/` structure, especially `docs/adr/` and `docs/guides/`
- Any existing `docs/agents/` files
- Any existing `.scratch/` directory

Present a short summary: what's present, what's missing, what will be created.

### 2. OKF template

Offer a template based on the repo. If the repo looks data-heavy, default to **Data**. Otherwise default to **Generic**.

**Generic:**

```
docs/app/
├── index.md
├── log.md
├── concepts/
├── decisions/
├── systems/
└── playbooks/
```

**Data:**

```
docs/app/
├── index.md
├── log.md
├── concepts/
├── decisions/
├── datasets/
├── tables/
├── pipelines/
└── playbooks/
```

Ask the user to confirm, swap, or customize.

### 3. Create the OKF bundle

- Create `docs/app/` and the chosen subdirectories.
- Create `docs/app/index.md` and `docs/app/log.md`.
- If `README.md` exists, merge its content into `docs/app/index.md` but keep `README.md`.
- If `CONTEXT.md` exists, merge its content into `docs/app/index.md` as a glossary/concepts section.
- Do **not** touch `guides/` or `docs/guides/`.
- Migrate existing ADRs from `docs/adr/` into `docs/app/decisions/` as OKF concept files, then remove the original ADR files.
- Update `docs/app/index.md` to list the new concept directories.
- Append an initialization entry to `docs/app/log.md`.

### 4. Issue tracker

Choose the tracker:

- **GitHub** — requires `git remote` pointing to GitHub and the `gh` CLI.
- **GitLab** — requires `git remote` pointing to GitLab and the `glab` CLI.
- **Local markdown** — issues under `.scratch/<feature-slug>/`.

If GitHub/GitLab is chosen, ask:

> Should external PRs also be treated as a triage surface? (yes / no, default: no)

Confirm the choice and write `docs/agents/issue-tracker.md`.

### 5. Triage labels

Use the five canonical roles from `setup-matt-pocock-skills`:

- `needs-triage`
- `needs-info`
- `ready-for-agent`
- `ready-for-human`
- `wontfix`

Ask if the repo already uses different label strings. Write `docs/agents/triage-labels.md` with the mapping.

### 6. Domain docs

Confirm the layout:

- **Single-context** — `docs/app/` holds the OKF bundle; domain terms under `docs/app/concepts/`, decisions under `docs/app/decisions/`.

Write `docs/agents/domain.md` describing the layout.

### 7. OKF agent instructions

Write `docs/agents/okf.md` telling other skills how to read and write OKF in this repo. Include:

- This repo uses OKF v0.1 under `docs/app/`.
- Concepts are markdown files with YAML frontmatter; `type` is required.
- Reserved filenames: `docs/app/index.md`, `docs/app/log.md`.
- Cross-links should be bundle-relative from `docs/app/` (e.g., `/concepts/order.md`).
- New domain terms go under `docs/app/concepts/`.
- New design decisions go under `docs/app/decisions/`.
- After adding or changing a concept, update `docs/app/index.md` and append to `docs/app/log.md`.
- Include the concept templates from `/grill-okf`.
- Mention that `/refer-okf` is the preferred skill for querying OKF and that other skills should rely on it for OKF-backed answers.

### 8. Agent skills block

Edit `CLAUDE.md` or `AGENTS.md` (whichever exists; ask if neither exists) and add an `## Agent skills` block:

```markdown
## Agent skills

### Issue tracker

[one-line summary]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary]. See `docs/agents/triage-labels.md`.

### Domain docs

OKF knowledge base under `docs/app/`. Query it with `/refer-okf`. See `docs/agents/domain.md` and `docs/agents/okf.md`.
```

If the block already exists, update it in place.

### 9. Run /grill-okf

Run `/grill-okf` to initiate the project. Ask the user what to grill first: the overall purpose, the domain model, or a concrete feature. The user may decline, but it is the default next step.

## Done

Tell the user the project is set up and which files were created. Mention that `docs/agents/*.md` can be edited directly later.
