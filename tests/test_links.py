from pathlib import Path

from tools.okf.links import validate


def test_valid_fixture_has_no_issues(tmp_path: Path):
    import shutil
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    result = validate(dst)
    assert result["broken"] == []
    assert result["orphans"] == []
    assert result["missing_frontmatter"] == []


def test_broken_link_and_orphan_and_missing_frontmatter(tmp_path: Path):
    import shutil
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    concepts = dst / "docs" / "app" / "concepts" / "orders"
    # Add broken link
    order_md = concepts / "order.md"
    order_md.write_text(order_md.read_text(encoding="utf-8") + "\n- [Missing](/concepts/orders/missing.md)\n", encoding="utf-8")
    # Add orphan concept
    (concepts / "orphan.md").write_text("---\ntype: Concept\ntitle: Orphan\ndescription: No links here.\ntimestamp: 2026-06-30T00:00:00Z\n---\n\nbody\n", encoding="utf-8")
    # Add missing frontmatter
    (concepts / "bad.md").write_text("---\ntitle: Bad\n---\n\nbody\n", encoding="utf-8")

    result = validate(dst)
    assert any("missing" in b.lower() for b in result["broken"])
    assert any("orphan.md" in o for o in result["orphans"])
    assert any("bad.md" in m for m in result["missing_frontmatter"])
