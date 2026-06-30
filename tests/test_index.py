from pathlib import Path

from tools.okf.index import regenerate
from tools.okf.paths import bundle_root


def test_regenerate_indexes(tmp_path: Path):
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    # Copy fixture into temp path to avoid mutating committed fixture
    import shutil
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    updated = regenerate(dst)
    assert bundle_root(dst) / "index.md" in updated
    assert bundle_root(dst) / "concepts" / "orders" / "index.md" in updated
    assert bundle_root(dst) / "decisions" / "index.md" in updated

    root_idx = (bundle_root(dst) / "index.md").read_text(encoding="utf-8")
    assert "Order" in root_idx
    assert "Customer" in root_idx
    assert "Use PostgreSQL" in root_idx

    sub_idx = (bundle_root(dst) / "concepts" / "orders" / "index.md").read_text(encoding="utf-8")
    assert "Customer" in sub_idx
    assert "Order" in sub_idx
