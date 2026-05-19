"""Tests for slicer.spec_loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from slicer.spec_loader import RepeatGroup, ScalarField, load_spec, spec_total_length


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_basic_parse(tmp_path: Path):
    spec = write(tmp_path / "h.spec", "prefix 4\nservice_code 6\n")
    items = load_spec(spec)
    assert items == [ScalarField("prefix", 4), ScalarField("service_code", 6)]


def test_comments_and_blank_lines_ignored(tmp_path: Path):
    spec = write(
        tmp_path / "h.spec",
        "# leading comment\n\nprefix 4   # trailing comment\n\nservice_code 6\n",
    )
    items = load_spec(spec)
    assert items == [ScalarField("prefix", 4), ScalarField("service_code", 6)]


def test_whitespace_between_name_and_length_is_flexible(tmp_path: Path):
    spec = write(tmp_path / "h.spec", "prefix\t\t4\nservice_code      6\n")
    assert load_spec(spec) == [ScalarField("prefix", 4), ScalarField("service_code", 6)]


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
    spec = write(tmp_path / "h.spec", "amount 13 numeric\nstatus 2 enum:OK,KO\n")
    assert load_spec(spec) == [ScalarField("amount", 13), ScalarField("status", 2)]


def test_unknown_trailing_token_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "amount 13 weirdtoken\n")
    with pytest.raises(ValueError, match="unexpected token"):
        load_spec(spec)


def test_spec_total_length_scalars():
    fields = [ScalarField("a", 4), ScalarField("b", 8), ScalarField("c", 6)]
    assert spec_total_length(fields) == 18


# -- @repeat block ----------------------------------------------------------


def test_repeat_block_parses(tmp_path: Path):
    spec = write(
        tmp_path / "h.spec",
        "lead 5\n@repeat records 3\n  break 4\n  cif 16\n  status 2\n@end\ntrailer 4\n",
    )
    items = load_spec(spec)
    assert len(items) == 3
    assert items[0] == ScalarField("lead", 5)
    assert isinstance(items[1], RepeatGroup)
    assert items[1].name == "records"
    assert items[1].count == 3
    assert items[1].fields == (
        ScalarField("break", 4),
        ScalarField("cif", 16),
        ScalarField("status", 2),
    )
    assert items[2] == ScalarField("trailer", 4)


def test_repeat_total_length(tmp_path: Path):
    spec = write(
        tmp_path / "h.spec",
        "lead 5\n@repeat records 3\n  break 4\n  cif 16\n  status 2\n@end\n",
    )
    # 5 + 3 * (4+16+2) = 5 + 66 = 71
    assert spec_total_length(load_spec(spec)) == 71


def test_repeat_requires_name_and_count(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "@repeat records\n  x 1\n@end\n")
    with pytest.raises(ValueError, match="@repeat <name> <count>"):
        load_spec(spec)


def test_repeat_count_must_be_positive_integer(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "@repeat records 0\n  x 1\n@end\n")
    with pytest.raises(ValueError, match="positive"):
        load_spec(spec)

    spec2 = write(tmp_path / "bad2.spec", "@repeat records abc\n  x 1\n@end\n")
    with pytest.raises(ValueError, match="integer"):
        load_spec(spec2)


def test_repeat_unterminated_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "@repeat records 3\n  x 1\n")
    with pytest.raises(ValueError, match="unterminated"):
        load_spec(spec)


def test_end_without_repeat_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "lead 4\n@end\n")
    with pytest.raises(ValueError, match="without matching"):
        load_spec(spec)


def test_nested_repeat_raises(tmp_path: Path):
    spec = write(
        tmp_path / "bad.spec",
        "@repeat outer 2\n  x 4\n  @repeat inner 2\n    y 2\n  @end\n@end\n",
    )
    with pytest.raises(ValueError, match="nested"):
        load_spec(spec)


def test_empty_repeat_block_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "@repeat records 3\n@end\n")
    with pytest.raises(ValueError, match="no fields"):
        load_spec(spec)


def test_duplicate_field_inside_repeat_raises(tmp_path: Path):
    spec = write(
        tmp_path / "bad.spec",
        "@repeat records 3\n  x 4\n  x 2\n@end\n",
    )
    with pytest.raises(ValueError, match="duplicate"):
        load_spec(spec)


def test_unknown_directive_raises(tmp_path: Path):
    spec = write(tmp_path / "bad.spec", "@nope something\n")
    with pytest.raises(ValueError, match="unknown directive"):
        load_spec(spec)
