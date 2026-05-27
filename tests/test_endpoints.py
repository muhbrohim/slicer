"""Tests for slicer.endpoints."""

from __future__ import annotations

from pathlib import Path

import pytest

from slicer.endpoints import (
    by_service_code,
    by_url,
    index_by_service_code,
    load_endpoints,
)


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


SAMPLE = """\
# comment line
# url                                 section  cat   service_code
/card/online-card-inquiry             3.1      CA    #CA1015
/card/cash-transaction-add            3.9      CA    #CA1017
/card/card-pin-set                    3.20     ANI   ANI6000

"""


def test_load_endpoints_skips_blanks_and_comments(tmp_path: Path):
    p = write(tmp_path / "endpoints.txt", SAMPLE)
    eps = load_endpoints(p)
    assert len(eps) == 3
    assert eps[0].url == "/card/online-card-inquiry"
    assert eps[0].section == "3.1"
    assert eps[0].category == "CA"
    assert eps[0].service_code == "#CA1015"


def test_malformed_row_raises(tmp_path: Path):
    p = write(tmp_path / "bad.txt", "/x only-three columns\n")
    with pytest.raises(ValueError, match="expected 4 columns"):
        load_endpoints(p)


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_endpoints(tmp_path / "nope.txt")


def test_by_service_code_tolerant(tmp_path: Path):
    eps = load_endpoints(write(tmp_path / "e.txt", SAMPLE))
    assert by_service_code("CA1017", eps).url == "/card/cash-transaction-add"
    assert by_service_code("#CA1017", eps).url == "/card/cash-transaction-add"
    assert by_service_code("ca1017", eps).url == "/card/cash-transaction-add"
    assert by_service_code("nope", eps) is None
    assert by_service_code("", eps) is None


def test_by_url(tmp_path: Path):
    eps = load_endpoints(write(tmp_path / "e.txt", SAMPLE))
    assert by_url("/card/cash-transaction-add", eps).service_code == "#CA1017"
    assert by_url("/no/such", eps) is None


def test_index_by_service_code(tmp_path: Path):
    eps = load_endpoints(write(tmp_path / "e.txt", SAMPLE))
    idx = index_by_service_code(eps)
    assert "CA1017" in idx
    assert "ANI6000" in idx
    assert idx["CA1017"].url == "/card/cash-transaction-add"
