"""Tests for slicer.programs."""

from __future__ import annotations

from pathlib import Path

import pytest

from slicer.programs import (
    by_service_code,
    index_by_service_code,
    load_programs,
)


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


# Tab-separated; spaces inside description are fine.
SAMPLE = (
    "#CA1010\tCASH AVAILABLE INQUIRY\tLHBSC10S\t1\tY\t20260127\t17445057\tSCSECOFR\n"
    "#US1003\tCUSTOMER SEARCH\tLHBSU03S\t1\tY\t20260421\t16382670\tZHAO HU\n"
    "\n"  # blank line skipped
    "#AC0042\tTEMPORARY CREDIT LIMIT UPDATE\tSCDSA42S\t1\tY\t20251118\t19253870\tSCSECOFR\n"
)


def test_load_programs_basic(tmp_path: Path):
    p = write(tmp_path / "pgm.tsv", SAMPLE)
    pgms = load_programs(p)
    assert len(pgms) == 3
    assert pgms[0].service_code == "#CA1010"
    assert pgms[0].name == "LHBSC10S"
    assert pgms[0].description == "CASH AVAILABLE INQUIRY"
    assert pgms[1].user == "ZHAO HU"  # spaces preserved within field


def test_malformed_row_raises(tmp_path: Path):
    p = write(tmp_path / "bad.tsv", "#X\tonly\tfive\tcolumns\there\n")
    with pytest.raises(ValueError, match="expected 8 tab-separated columns"):
        load_programs(p)


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_programs(tmp_path / "nope.tsv")


def test_by_service_code_tolerant(tmp_path: Path):
    pgms = load_programs(write(tmp_path / "p.tsv", SAMPLE))
    assert by_service_code("CA1010", pgms).name == "LHBSC10S"
    assert by_service_code("#CA1010", pgms).name == "LHBSC10S"
    assert by_service_code("ca1010", pgms).name == "LHBSC10S"
    assert by_service_code("nope", pgms) is None
    assert by_service_code("", pgms) is None


def test_index_by_service_code(tmp_path: Path):
    pgms = load_programs(write(tmp_path / "p.tsv", SAMPLE))
    idx = index_by_service_code(pgms)
    assert "CA1010" in idx
    assert idx["CA1010"].name == "LHBSC10S"
    assert idx["AC0042"].name == "SCDSA42S"
