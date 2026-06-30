"""Extract and validate OKF cross-links."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .document import read
from .index import iter_concepts
from .paths import bundle_root


def extract_link_targets(cwd: Path = Path(".")) -> dict[Path, list[str]]:
    root = bundle_root(cwd)
    result: dict[Path, list[str]] = {}
    for doc in iter_concepts(root):
        result[doc.path] = doc.links()
    return result


def validate(cwd: Path = Path(".")) -> dict[str, list[str]]:
    root = bundle_root(cwd)
    if not root.exists():
        return {"missing_bundle": [str(root)]}

    docs = list(iter_concepts(root))
    existing = {_normalize(root, d.path) for d in docs}

    broken: list[str] = []
    orphans: list[str] = []

    for doc in docs:
        for link in doc.links():
            target = _resolve(root, link)
            if target not in existing:
                broken.append(f"{doc.path.relative_to(root).as_posix()} -> {link}")

    linked_to: set[str] = set()
    for doc in docs:
        for link in doc.links():
            linked_to.add(_resolve(root, link))

    for doc in docs:
        rel = _normalize(root, doc.path)
        if linked_to and rel not in linked_to and not rel.startswith("/index"):
            orphans.append(rel)

    return {"broken": broken, "orphans": orphans}


def _normalize(root: Path, path: Path) -> str:
    return "/" + path.relative_to(root).as_posix()


def _resolve(root: Path, link: str) -> str:
    """Bundle-relative link target without .md extension."""
    link = link.split("#")[0]
    if link.endswith("/"):
        link += "index.md"
    if not link.endswith(".md"):
        link += ".md"
    return link
