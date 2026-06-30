"""OKF bundle path conventions."""
from pathlib import Path

BUNDLE_ROOT = Path("docs/app")
INDEX_FILE = "index.md"
LOG_FILE = "log.md"
SPEC_FILE = "docs/agents/okf-spec.md"


def bundle_root(cwd: Path = Path(".")) -> Path:
    return cwd / BUNDLE_ROOT


def index_path(dirpath: Path) -> Path:
    return dirpath / INDEX_FILE


def log_path(cwd: Path = Path(".")) -> Path:
    return bundle_root(cwd) / LOG_FILE


def is_reserved(name: str) -> bool:
    return name in (INDEX_FILE, LOG_FILE)


def concept_dirs() -> tuple[str, ...]:
    return ("concepts", "decisions", "systems", "datasets", "tables", "pipelines", "playbooks")
