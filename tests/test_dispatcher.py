"""Tests for slicer.dispatcher.parse_message."""

from __future__ import annotations

from pathlib import Path

import pytest

from slicer.dispatcher import parse_message


@pytest.fixture()
def specs_root(tmp_path: Path) -> Path:
    """A fully-formed specs root: header.spec + body/CA1017.spec."""
    (tmp_path / "body").mkdir()
    (tmp_path / "header.spec").write_text(
        "prefix 4\nchannel 8\nservice_code 6\ndevice 20\n", encoding="utf-8"
    )
    (tmp_path / "body" / "CA1017.spec").write_text(
        "transaction_id 12\namount 13\nresponse_code 2\ncustomer_name 30\n",
        encoding="utf-8",
    )
    return tmp_path


def _build_sample(customer_name: str = "JOHN DOE") -> str:
    parts = [
        "ADSV",
        "MOBILE".ljust(8),
        "CA1017",
        "DEVICE-001-ABCDEFGH".ljust(20),
        "TRX000000001",
        "0000000001350",
        "00",
        customer_name.ljust(30),
    ]
    return "".join(parts)


def test_happy_path(specs_root: Path):
    result = parse_message(_build_sample(), specs_root)

    assert result.service_code == "CA1017"
    assert result.errors == []
    assert result.warnings == []
    assert result.unparsed_tail is None

    header = {f.name: f.value for f in result.header}
    body = {f.name: f.value for f in result.body}

    assert header["prefix"] == "ADSV"
    assert header["channel"] == "MOBILE  "
    assert header["service_code"] == "CA1017"
    assert header["device"] == "DEVICE-001-ABCDEFGH "

    assert body["transaction_id"] == "TRX000000001"
    assert body["amount"] == "0000000001350"
    assert body["response_code"] == "00"
    assert body["customer_name"] == "JOHN DOE".ljust(30)


def test_missing_header_spec_errors(tmp_path: Path):
    result = parse_message("anything", tmp_path)
    assert result.service_code is None
    assert result.header == []
    assert any("Missing header.spec" in e for e in result.errors)


def test_missing_service_code_field_in_header(tmp_path: Path):
    (tmp_path / "body").mkdir()
    (tmp_path / "header.spec").write_text("prefix 4\nchannel 8\n", encoding="utf-8")
    result = parse_message("ADSVMOBILE  ", tmp_path)
    assert result.service_code is None
    assert any("missing 'service_code' field" in e for e in result.errors)


def test_missing_body_spec_emits_warning_and_keeps_header(specs_root: Path):
    # Build a header for an unknown service code.
    message = "ADSV" + "MOBILE".ljust(8) + "CA9999" + "DEVICE-001-ABCDEFGH".ljust(20) + "JUNK"
    result = parse_message(message, specs_root)

    assert result.service_code == "CA9999"
    assert any("Missing body spec" in w for w in result.warnings)
    assert result.body == []
    assert result.unparsed_tail == "JUNK"
    assert result.errors == []


def test_truncated_message_in_body(specs_root: Path):
    # Header (38) + partial body — cut off mid-amount.
    truncated = _build_sample()[:50]  # past header, mid-body
    result = parse_message(truncated, specs_root)

    assert result.service_code == "CA1017"
    assert any("truncated" in e.lower() for e in result.errors)
    # Truncation should not crash; we keep whatever parsed.
    assert result.body  # at least transaction_id likely landed


def test_overflow_emits_warning_and_exposes_tail(specs_root: Path):
    message = _build_sample() + "EXTRA-TRAILING"
    result = parse_message(message, specs_root)

    assert result.service_code == "CA1017"
    assert any("Extra trailing payload" in w for w in result.warnings)
    assert result.unparsed_tail == "EXTRA-TRAILING"


def test_result_as_dict_is_json_safe(specs_root: Path):
    import json

    result = parse_message(_build_sample(), specs_root)
    # Round-trip through json — should not raise.
    payload = json.dumps(result.as_dict())
    reloaded = json.loads(payload)
    assert reloaded["service_code"] == "CA1017"
    assert reloaded["header"]["prefix"] == "ADSV"
    assert reloaded["body"]["amount"] == "0000000001350"
