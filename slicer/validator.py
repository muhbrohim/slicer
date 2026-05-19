"""Field validation hooks.

v0.1 only enforces length implicitly (via truncation detection in the parser).
The hooks below are stubs / placeholders so v0.2's typed validation has a
single integration point.
"""

from __future__ import annotations

from slicer.models import ParseResult


def validate(result: ParseResult) -> ParseResult:
    """Run validation passes over a parsed result, appending warnings/errors.

    v0.1: no-op. Returns `result` unchanged. Reserved for numeric/required/
    date/enum checks in v0.2.
    """
    return result
