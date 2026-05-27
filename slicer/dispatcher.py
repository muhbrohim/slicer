"""Orchestrates the header -> service_code -> body parse pipeline."""

from __future__ import annotations

from pathlib import Path

from slicer.models import ParseResult
from slicer.parser import sequential_parse
from slicer.spec_loader import ScalarField, load_spec

SERVICE_CODE_FIELD = "service_code"


def parse_message(
    message: str,
    specs_dir: str | Path,
) -> ParseResult:
    """Parse `message` using `specs_dir/header.spec` and the matching body spec.

    Never raises on malformed input — errors/warnings are accumulated on the
    returned ParseResult so callers (CLI, tests, scripts) can react uniformly.
    """
    result = ParseResult()
    specs_root = Path(specs_dir)
    header_path = specs_root / "header.spec"

    if not header_path.is_file():
        result.errors.append(f"Missing header.spec at {header_path}")
        return result

    try:
        header_fields = load_spec(header_path)
    except (ValueError, FileNotFoundError) as exc:
        result.errors.append(str(exc))
        return result

    header_parsed, pos_after_header, header_errors = sequential_parse(message, header_fields)
    result.header = header_parsed
    result.errors.extend(header_errors)

    service_code = _extract_service_code(result)
    if service_code is None:
        # Truncated header may legitimately have no service_code, but the
        # spec itself must always define one — that case is a hard error.
        if not any(
            isinstance(item, ScalarField) and item.name == SERVICE_CODE_FIELD
            for item in header_fields
        ):
            result.errors.append("header.spec missing 'service_code' field")
        return result

    result.service_code = service_code

    # If the header itself was truncated, there is no body to parse —
    # the leftover bytes belong to the header, not to the body.
    if header_errors:
        return result

    body_path = specs_root / "body" / f"{service_code}.spec"
    if not body_path.is_file():
        result.warnings.append(f"Missing body spec: {body_path.name}")
        tail = message[pos_after_header:]
        result.unparsed_tail = tail or None
        return result

    try:
        body_fields = load_spec(body_path)
    except (ValueError, FileNotFoundError) as exc:
        result.errors.append(str(exc))
        result.unparsed_tail = message[pos_after_header:] or None
        return result

    # Surface structured metadata from the body spec (endpoint, category, …).
    meta = getattr(body_fields, "metadata", {}) or {}
    result.endpoint = meta.get("endpoint") or None
    if result.endpoint == "<none>":
        result.endpoint = None
    result.category = meta.get("category") or None
    if result.category == "-":
        result.category = None
    result.section = meta.get("section") or None
    if result.section == "-":
        result.section = None
    result.program = meta.get("program") or None
    if result.program == "<none>":
        result.program = None

    body_parsed, pos_after_body, body_errors = sequential_parse(
        message, body_fields, start_pos=pos_after_header
    )
    result.body = body_parsed
    result.errors.extend(body_errors)

    if pos_after_body < len(message):
        overflow = len(message) - pos_after_body
        result.warnings.append(f"Extra trailing payload detected ({overflow} bytes)")
        result.unparsed_tail = message[pos_after_body:]

    return result


def _extract_service_code(result: ParseResult) -> str | None:
    for parsed in result.header:
        if parsed.name == SERVICE_CODE_FIELD:
            value = parsed.value.strip()
            return value or None
    return None
