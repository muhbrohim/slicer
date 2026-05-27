"""Tests for scripts/backfill_spec_headers.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    path = ROOT / "scripts" / "backfill_spec_headers.py"
    spec = importlib.util.spec_from_file_location("backfill_spec_headers", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["backfill_spec_headers"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def backfill():
    return _load_module()


def test_strip_owned_metadata_removes_block(backfill):
    lines = [
        "# service-code: #CA1017",
        "# endpoint:     /x",
        "# category:     CA",
        "# section:      3.9",
        "#",
        "# prose comment",
        "prefix 4",
    ]
    out = backfill.strip_owned_metadata(lines)
    assert out == ["# prose comment", "prefix 4"]


def test_strip_is_idempotent_on_clean_file(backfill):
    lines = ["# prose only", "prefix 4"]
    assert backfill.strip_owned_metadata(lines) == lines


def test_process_spec_is_idempotent(tmp_path, backfill):
    from slicer.endpoints import Endpoint, index_by_service_code

    body_dir = tmp_path / "body"
    body_dir.mkdir()
    spec = body_dir / "#CA1017.spec"
    spec.write_text("# prose\nprefix 4\nservice_code 6\n", encoding="utf-8")

    eps = [Endpoint(url="/card/cash-transaction-add", section="3.9",
                    category="CA", service_code="#CA1017")]
    idx = index_by_service_code(eps)

    o1, content1 = backfill.process_spec(spec, idx)
    spec.write_text(content1, encoding="utf-8")
    o2, content2 = backfill.process_spec(spec, idx)
    assert o2.status == "unchanged"
    assert content1 == content2
    assert "# endpoint:     /card/cash-transaction-add" in content1
