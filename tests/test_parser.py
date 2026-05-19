"""Tests for slicer.parser.sequential_parse."""

from __future__ import annotations

from slicer.parser import sequential_parse


def test_parses_all_fields_in_order():
    message = "ADSVMOBILE  CA1017"
    fields = [("prefix", 4), ("channel", 8), ("service_code", 6)]

    parsed, pos, errors = sequential_parse(message, fields)

    assert [p.name for p in parsed] == ["prefix", "channel", "service_code"]
    assert [p.value for p in parsed] == ["ADSV", "MOBILE  ", "CA1017"]
    assert [(p.start, p.end) for p in parsed] == [(0, 3), (4, 11), (12, 17)]
    assert pos == 18
    assert errors == []


def test_offsets_are_zero_indexed_and_inclusive():
    parsed, _pos, _errors = sequential_parse("abcde", [("x", 2), ("y", 3)])
    assert parsed[0].start == 0
    assert parsed[0].end == 1
    assert parsed[1].start == 2
    assert parsed[1].end == 4


def test_truncation_emits_error_and_stops_parsing():
    parsed, pos, errors = sequential_parse("ABCDE", [("a", 3), ("b", 5)])
    assert [p.name for p in parsed] == ["a"]
    assert pos == 3
    assert len(errors) == 1
    assert "truncated" in errors[0].lower()
    assert "'b'" in errors[0]


def test_start_pos_offsets_into_message():
    message = "HEADERBODY"
    parsed, pos, errors = sequential_parse(message, [("body", 4)], start_pos=6)
    assert parsed[0].value == "BODY"
    assert (parsed[0].start, parsed[0].end) == (6, 9)
    assert pos == 10
    assert errors == []


def test_empty_fields_returns_empty():
    parsed, pos, errors = sequential_parse("ABC", [], start_pos=2)
    assert parsed == []
    assert pos == 2
    assert errors == []


def test_overflow_is_not_an_error_at_parser_level():
    # The parser itself only reports truncation; overflow is a dispatcher concern.
    parsed, pos, errors = sequential_parse("ABCDEFG", [("x", 3)])
    assert parsed[0].value == "ABC"
    assert pos == 3
    assert errors == []
