"""Tests for slicer.spec_loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from slicer.spec_loader import load_spec, spec_total_length


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_basic_parse(tmp_path: Path):
    spec = write(tmp_path / "h.spec", "prefix 4\nservice_code 6\n")
    assert load_spec(spec) == [("prefix", 4), ("service_code", 6)]


def test_comments_and_blank_lines_ignored(tmp_path: Path):
    spec = write(
        tmp_path / "h.spec",
        "# leading comment\n\nprefix 4   # trailing comment\n\nservice_code 6\n",
    )
    assert load_spec(spec) == [("prefix", 4), ("service_code", 6)]


def test_whitespace_between_name_and_length_is_flexible(tmp_path: Path):
    spec = write(tmp_path / "h.spec", "prefix\t\t4\nservice_code      6\n")
    assert load_spec(spec) == [("prefix", 4), ("service_code", 6)]


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_spec(tmp_path / "does-not-exist.spec")


def test_non_integer_length_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "prefix four\n")
    with pytest.raises(ValueError, match="length must be an integer"):
        load_spec(spec)


def test_non_positive_length_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "prefix 0\n")
    with pytest.raises(ValueError, match="positive"):
        load_spec(spec)


def test_missing_length_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "lonely_field\n")
    with pytest.raises(ValueError, match="expected"):
        load_spec(spec)


def test_duplicate_field_name_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "x 3\nx 4\n")
    with pytest.raises(ValueError, match="duplicate"):
        load_spec(spec)


def test_empty_spec_raises(tmp_path: Path):
    spec = write(tmp_path / "empty.spec", "# only comments\n\n")
    with pytest.raises(ValueError, match="empty"):
        load_spec(spec)


def test_v02_type_hints_are_accepted_as_passthrough(tmp_path: Path):
    # Should not raise — type hints are reserved for v0.2 but the loader
    # must tolerate them today so specs stay forward-compatible.
    spec = write(tmp_path / "h.spec", "amount 13 numeric\nstatus 2 enum:OK,KO\n")
    assert load_spec(spec) == [("amount", 13), ("status", 2)]


def test_unknown_trailing_token_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "amount 13 weirdtoken\n")
    with pytest.raises(ValueError, match="unexpected token"):
        load_spec(spec)


def test_spec_total_length():
    fields = [("a", 4), ("b", 8), ("c", 6)]
    assert spec_total_length(fields) == 18
