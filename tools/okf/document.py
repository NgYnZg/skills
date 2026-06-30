"""Parse and serialize OKF concept documents."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_KEYS = ("type", "title", "description", "timestamp")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


try:
    import yaml

    def _parse_yaml(text: str) -> dict[str, Any]:
        return yaml.safe_load(text) or {}

    def _dump_yaml(data: dict[str, Any]) -> str:
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True).rstrip()

except Exception:  # pragma: no cover - lazy fallback if PyYAML missing
    def _parse_yaml(text: str) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for line in text.splitlines():
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            data[key] = value
        return data

    def _dump_yaml(data: dict[str, Any]) -> str:
        lines = []
        for key, value in data.items():
            if isinstance(value, str) and (
                ":" in value or value.startswith("'") or value.startswith('"')
            ):
                value = f'"{value.replace(chr(34), chr(92) + chr(34))}"'
            lines.append(f"{key}: {value}")
        return "\n".join(lines)


@dataclass
class Document:
    path: Path
    frontmatter: dict[str, Any]
    body: str

    def type(self) -> str | None:
        return self.frontmatter.get("type")

    def title(self) -> str | None:
        return self.frontmatter.get("title")

    def description(self) -> str | None:
        return self.frontmatter.get("description")

    def links(self) -> list[str]:
        """Return bundle-relative link targets found in the body."""
        found: list[str] = []
        for match in re.finditer(r"\[([^\]]+)\]\((/[^)]+)\)", self.body):
            found.append(match.group(2))
        return found

    def missing_required_keys(self) -> list[str]:
        return [k for k in REQUIRED_KEYS if k not in self.frontmatter]

    def to_text(self) -> str:
        fm = _dump_yaml(self.frontmatter)
        body = self.body
        if body and not body.startswith("\n"):
            body = "\n" + body
        if body and not body.endswith("\n"):
            body += "\n"
        return f"---\n{fm}\n---{body}"


def parse(text: str, path: Path | None = None) -> Document:
    path = path or Path("unknown.md")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return Document(path=path, frontmatter={}, body=text)
    return Document(path=path, frontmatter=_parse_yaml(match.group(1)), body=match.group(2))


def read(path: Path) -> Document:
    return parse(path.read_text(encoding="utf-8"), path)


def write(doc: Document) -> None:
    doc.path.write_text(doc.to_text(), encoding="utf-8")


def touch(path: Path, doc_type: str, title: str, description: str) -> Document:
    """Create or overwrite a minimal OKF concept file."""
    doc = Document(
        path=path,
        frontmatter={
            "type": doc_type,
            "title": title,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        body="\n",
    )
    write(doc)
    return doc
