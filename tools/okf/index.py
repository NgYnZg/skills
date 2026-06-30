"""Regenerate OKF index.md files."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .document import read, Document
from .paths import bundle_root, index_path, is_reserved, concept_dirs


def iter_concepts(root: Path) -> Iterable[Document]:
    for path in root.rglob("*.md"):
        if path.name in ("index.md", "log.md"):
            continue
        yield read(path)


def _rel(bundle: Path, path: Path) -> str:
    rel = path.relative_to(bundle).as_posix()
    return "/" + rel


def _dir_summary(root: Path, dirpath: Path, docs: list[Document]) -> str:
    lines = [f"# {dirpath.name}", ""]
    if not docs:
        lines.append("No concepts yet.")
        return "\n".join(lines) + "\n"

    by_type: dict[str, list[Document]] = {}
    for doc in docs:
        by_type.setdefault(doc.type() or "Concept", []).append(doc)

    for t in sorted(by_type):
        lines.append(f"## {t}")
        lines.append("")
        for doc in sorted(by_type[t], key=lambda d: d.title() or d.path.stem):
            rel = _rel(root, doc.path)
            title = doc.title() or doc.path.stem
            desc = doc.description() or ""
            lines.append(f"- [{title}]({rel}) — {desc}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def regenerate(cwd: Path = Path(".")) -> list[Path]:
    root = bundle_root(cwd).resolve()
    if not root.exists():
        raise FileNotFoundError(f"OKF bundle not found at {root}")

    # Collect docs per directory
    dir_docs: dict[Path, list[Document]] = {}
    for doc in iter_concepts(root):
        dir_docs.setdefault(doc.path.parent, []).append(doc)

    updated: list[Path] = []

    # Write subdirectory indexes
    for dirpath in sorted(dir_docs):
        idx = index_path(dirpath)
        idx.write_text(_dir_summary(root, dirpath, dir_docs[dirpath]), encoding="utf-8")
        updated.append(idx)

    # Write root index
    root_idx = index_path(root)
    root_text = ["# OKF Knowledge Base", ""]
    root_text.append("Auto-generated index. See `docs/app/log.md` for changes.")
    root_text.append("")

    # Inline subdirectory indexes
    for dirpath in sorted(dir_docs):
        rel = dirpath.relative_to(root).as_posix()
        root_text.append(f"## {rel}")
        root_text.append("")
        for doc in sorted(dir_docs[dirpath], key=lambda d: d.title() or d.path.stem):
            rel_doc = _rel(root, doc.path)
            title = doc.title() or doc.path.stem
            desc = doc.description() or ""
            root_text.append(f"- [{title}]({rel_doc}) — {desc}")
        root_text.append("")

    root_idx.write_text("\n".join(root_text).rstrip() + "\n", encoding="utf-8")
    updated.append(root_idx)

    return updated
