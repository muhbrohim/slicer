"""Tests for slicer.parser.sequential_parse."""

from __future__ import annotations

from slicer.parser import sequential_parse
from slicer.spec_loader import RepeatGroup, ScalarField


def test_parses_all_fields_in_order():
    message = "ADSVMOBILE  CA1017"
    spec = [
        ScalarField("prefix", 4),
        ScalarField("channel", 8),
        ScalarField("service_code", 6),
    ]

    parsed, pos, errors = sequential_parse(message, spec)

    assert [p.name for p in parsed] == ["prefix", "channel", "service_code"]
    assert [p.value for p in parsed] == ["ADSV", "MOBILE  ", "CA1017"]
    assert [(p.start, p.end) for p in parsed] == [(0, 3), (4, 11), (12, 17)]
    assert pos == 18
    assert errors == []


def test_offsets_are_zero_indexed_and_inclusive():
    parsed, _pos, _errors = sequential_parse("abcde", [ScalarField("x", 2), ScalarField("y", 3)])
    assert parsed[0].start == 0
    assert parsed[0].end == 1
    assert parsed[1].start == 2
    assert parsed[1].end == 4


def test_truncation_emits_error_and_stops_parsing():
    parsed, pos, errors = sequential_parse("ABCDE", [ScalarField("a", 3), ScalarField("b", 5)])
    assert [p.name for p in parsed] == ["a"]
    assert pos == 3
    assert len(errors) == 1
    assert "truncated" in errors[0].lower()
    assert "'b'" in errors[0]


def test_start_pos_offsets_into_message():
    message = "HEADERBODY"
    parsed, pos, errors = sequential_parse(message, [ScalarField("body", 4)], start_pos=6)
    assert parsed[0].value == "BODY"
    assert (parsed[0].start, parsed[0].end) == (6, 9)
    assert pos == 10
    assert errors == []


def test_empty_spec_returns_empty():
    parsed, pos, errors = sequential_parse("ABC", [], start_pos=2)
    assert parsed == []
    assert pos == 2
    assert errors == []


def test_overflow_is_not_an_error_at_parser_level():
    parsed, pos, errors = sequential_parse("ABCDEFG", [ScalarField("x", 3)])
    assert parsed[0].value == "ABC"
    assert pos == 3
    assert errors == []


# -- @repeat -----------------------------------------------------------------


def test_repeat_emits_indexed_field_names():
    # 3 records, each = break(4) + n(2) = 6 bytes. Total = 18.
    message = "=01=AB=02=CD=03=EF"
    spec = [
        RepeatGroup(
            name="records",
            count=3,
            fields=(ScalarField("break", 4), ScalarField("n", 2)),
        )
    ]
    parsed, pos, errors = sequential_parse(message, spec)
    assert [p.name for p in parsed] == [
        "records[01].break",
        "records[01].n",
        "records[02].break",
        "records[02].n",
        "records[03].break",
        "records[03].n",
    ]
    assert [p.value for p in parsed] == ["=01=", "AB", "=02=", "CD", "=03=", "EF"]
    assert pos == 18
    assert errors == []


def test_repeat_offsets_are_continuous():
    message = "ABCD" * 4
    spec = [RepeatGroup(name="g", count=4, fields=(ScalarField("v", 4),))]
    parsed, _pos, _errors = sequential_parse(message, spec)
    assert [(p.start, p.end) for p in parsed] == [(0, 3), (4, 7), (8, 11), (12, 15)]


def test_repeat_truncation_stops_at_partial_record():
    # 3 records of 4 bytes, but message is only 9 bytes — third record is
    # only partially present.
    message = "AAAABBBBC"
    spec = [RepeatGroup(name="g", count=3, fields=(ScalarField("v", 4),))]
    parsed, _pos, errors = sequential_parse(message, spec)
    assert [p.value for p in parsed] == ["AAAA", "BBBB"]
    assert len(errors) == 1
    assert "truncated" in errors[0].lower()


def test_mixed_scalar_and_repeat():
    message = "LEADXYZ=01=A=02=BTAIL"
    spec = [
        ScalarField("lead", 7),
        RepeatGroup("records", 2, (ScalarField("break", 4), ScalarField("v", 1))),
        ScalarField("tail", 4),
    ]
    parsed, pos, errors = sequential_parse(message, spec)
    names = [p.name for p in parsed]
    assert names == [
        "lead",
        "records[01].break",
        "records[01].v",
        "records[02].break",
        "records[02].v",
        "tail",
    ]
    assert pos == len(message)
    assert errors == []
