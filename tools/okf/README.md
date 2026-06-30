# okf-tool

Small OKF bundle helper. Copied into target repos by `/setup-okf` under `scripts/okf/`.

## Usage

```bash
python -m scripts.okf.cli index      # regenerate all index.md files
python -m scripts.okf.cli validate   # check frontmatter and links
python -m scripts.okf.cli log "..."  # append a log entry
python -m scripts.okf.cli viz        # generate docs/viz.html
python -m scripts.okf.cli show path/to/concept.md
```

No required dependencies beyond Python stdlib. PyYAML is used if installed; otherwise a minimal frontmatter parser handles simple key-value frontmatter.
