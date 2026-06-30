# OKF skills upgrade plan

Based on the gap analysis against the `knowledge-catalog` project, upgrade the three existing skills (`setup-okf`, `grill-okf`, `refer-okf`) by adding a small, reusable bundle tool and updating skill instructions. The BigQuery/source-adapter pieces are ignored because they are Google-specific.

## Guiding principles

- Keep skills markdown-first and Pi-native.
- Add one shared Python helper (`okf-tool`) for parsing, indexing, logging, validation, and visualization. The skills call it; they do not reimplement its logic.
- No new runtime dependencies in target repos beyond Python stdlib + the copied helper.
- Prefer lazy, reusable upgrades over domain-specific adapters.

## Proposed changes

### 1. Formalize the OKF spec

- Copy/summarize `okf/SPEC.md` from `knowledge-catalog` into a new file emitted by `/setup-okf`: `docs/agents/okf-spec.md`.
- Update `setup-okf/SKILL.md` step 8 to reference the spec and tell agents to follow it.
- Update `grill-okf/SKILL.md` and `refer-okf/SKILL.md` to point agents at `docs/agents/okf-spec.md`.

### 2. Create a shared `okf-tool` Python package

Add `tools/okf/` to this repo (or, simpler, one module per concern under `tools/okf/`):

- `tools/okf/document.py` — parse/serialize markdown with YAML frontmatter, enforce required keys (`type`, `title`, `description`, `timestamp`), preserve frontmatter ordering.
- `tools/okf/paths.py` — bundle layout constants and path helpers.
- `tools/okf/index.py` — scan `docs/app/`, group concepts by `type`, regenerate every `index.md` (root + per-context), synthesize directory descriptions.
- `tools/okf/log.py` — append dated entries to `docs/app/log.md` whenever a concept is written or changed.
- `tools/okf/links.py` — extract bundle-relative internal links, report dangling links and orphan concepts.
- `tools/okf/viewer.py` — generate a single self-contained `viz.html` with a force-directed graph, search, type filters, detail panel, and backlinks (port from `knowledge-catalog/viewer/`).
- `tools/okf/cli.py` — small `argparse` CLI wrapping the above:
  - `okf-tool index` — regenerate all `index.md` files.
  - `okf-tool validate` — check required frontmatter and report broken links.
  - `okf-tool log --message "..."` — append a log entry.
  - `okf-tool viz` — generate `viz.html`.

`setup-okf` will copy or symlink `tools/okf/` into the target repo (e.g. `.tools/okf/` or `scripts/okf/`) so the CLI is available there too.

### 3. Update `/setup-okf`

- Emit `docs/agents/okf-spec.md`.
- Copy the `okf-tool` package into the target repo under `scripts/okf/`.
- After creating or migrating concepts, run `okf-tool index` and `okf-tool validate` instead of hand-editing indexes.
- Replace manual `docs/app/log.md` appending with `okf-tool log`.
- Add a brief mention of `okf-tool viz` in the generated agent instructions.

### 4. Update `/grill-okf`

- After writing each concept, call `okf-tool log --message "Created/updated <path>"`.
- At the end of a grilling session, call `okf-tool index` to refresh all `index.md` files.
- Add optional `okf-tool validate` at the end to catch broken cross-links before finishing.
- Keep concept templates in `SKILL.md` but note that `okf-spec.md` is the authoritative reference.

### 5. Update `/refer-okf`

- Before answering, optionally run `okf-tool validate` and warn about broken links if any are found (does not block the answer).
- Mention that `viz.html` is available for browsing the knowledge graph.
- No major logic change; the skill stays read-only.

### 6. Add tests

Add a small pytest suite under `tests/`:

- `tests/test_document.py` — round-trip frontmatter parsing, missing keys, timestamp formatting.
- `tests/test_index.py` — index regeneration on a sample bundle.
- `tests/test_links.py` — detect a dangling link and an orphan concept.
- `tests/test_cli.py` — invoke each CLI subcommand in a temp directory.

Use a sample fixture bundle rather than a real repo.

### 7. Add sample bundles (optional)

- Keep one or two minimal example bundles under `examples/` in this repo so users can see expected output.
- This is lower priority than the tooling above.

### 8. Source adapters (future)

- Do not build now. When a concrete project needs it, add small adapters (OpenAPI, dbt, SQLAlchemy, Terraform) as separate `tools/okf/sources/<name>.py` modules.
- Each adapter scans source files and emits OKF concept files, then `okf-tool index` picks them up.

## Implementation order

1. Vendor/port `document.py`, `paths.py`, `index.py`, `log.py`, `links.py`, `cli.py` into `tools/okf/`.
2. Add tests for the bundle tool.
3. Update `setup-okf/SKILL.md` to emit the spec, copy the tool, and use it for index/log/validation.
4. Update `grill-okf/SKILL.md` and `refer-okf/SKILL.md` to reference the tool.
5. Add `docs/agents/okf-spec.md` template content to `setup-okf`.
6. Port `viewer.py` and add `okf-tool viz`.
7. Update `README.md` to document the tool and new capabilities.

## Acceptance criteria

- Running `/setup-okf` in a fresh repo produces `docs/agents/okf-spec.md` and a working `scripts/okf/` tool.
- `python -m scripts.okf.cli index` regenerates all `index.md` files in a sample bundle.
- `python -m scripts.okf.cli validate` reports missing frontmatter and broken links.
- `python -m scripts.okf.cli viz` produces a single `viz.html`.
- `/grill-okf` instructions tell the agent to run `okf-tool index` and `okf-tool log` after writing concepts.
- `/refer-okf` instructions mention `okf-tool validate` and `viz.html`.
- `pytest` passes for `document`, `index`, `links`, and `cli`.

## What to skip

- BigQuery/source adapters until a concrete project asks for them.
- Complex evaluation metrics; start with `validate` counts and the visualizer.
- Automatic grounding across all skills (README already documents this as a future enhancement).
