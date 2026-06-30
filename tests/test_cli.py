from pathlib import Path
import shutil

from tools.okf.cli import main


def test_cli_index_regenerates_indexes(tmp_path: Path):
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    assert main(["--cwd", str(dst), "index"]) == 0
    assert (dst / "docs" / "app" / "index.md").exists()


def test_cli_validate_reports_issues(tmp_path: Path):
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    concepts = dst / "docs" / "app" / "concepts" / "orders"
    order_md = concepts / "order.md"
    order_md.write_text(order_md.read_text(encoding="utf-8") + "\n- [Missing](/concepts/orders/missing.md)\n", encoding="utf-8")

    assert main(["--cwd", str(dst), "validate"]) == 1


def test_cli_log_appends_entry(tmp_path: Path):
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    assert main(["--cwd", str(dst), "log", "test entry"]) == 0
    log = (dst / "docs" / "app" / "log.md").read_text(encoding="utf-8")
    assert "test entry" in log


def test_cli_viz_generates_html(tmp_path: Path):
    sample = Path(__file__).parent / "fixtures" / "sample-bundle"
    dst = tmp_path / "bundle"
    shutil.copytree(sample, dst)

    assert main(["--cwd", str(dst), "viz"]) == 0
    assert (dst / "docs" / "viz.html").exists()
