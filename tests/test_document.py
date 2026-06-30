from pathlib import Path

from tools.okf.document import parse, REQUIRED_KEYS


def test_parse_frontmatter_and_body():
    text = """---
type: Concept
title: Order
description: A purchase.
timestamp: 2026-06-30T00:00:00Z
---

# Body

hello
"""
    doc = parse(text, Path("order.md"))
    assert doc.type() == "Concept"
    assert doc.title() == "Order"
    assert doc.description() == "A purchase."
    assert "# Body" in doc.body


def test_missing_required_keys():
    doc = parse("---\ntype: Concept\n---\n\nbody\n", Path("x.md"))
    assert doc.missing_required_keys() == ["title", "description", "timestamp"]


def test_round_trip_preserves_keys():
    text = """---
type: Decision
title: T
description: D
timestamp: 2026-06-30T00:00:00Z
---

body
"""
    doc = parse(text, Path("d.md"))
    out = doc.to_text()
    for key in REQUIRED_KEYS:
        assert key in out


def test_extract_bundle_relative_links():
    doc = parse(
        "---\ntype: Concept\ntitle: X\ndescription: Y\ntimestamp: 2026-06-30T00:00:00Z\n---\n\n- [A](/concepts/a.md)\n- [B](/decisions/b.md)\n",
        Path("x.md"),
    )
    assert doc.links() == ["/concepts/a.md", "/decisions/b.md"]
