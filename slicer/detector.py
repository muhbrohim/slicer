"""Fallback service_code detection.

If header parsing produces no `service_code` (e.g. header.spec is missing or
malformed), `detect_service_code` scans the raw message for any token that
matches a known body spec filename. This is best-effort and only used when the
dispatcher has already failed.
"""

from __future__ import annotations

import re
from pathlib import Path

_TOKEN_RE = re.compile(r"[A-Z]{2}\d{3,5}")


def detect_service_code(message: str, specs_dir: str | Path) -> str | None:
    """Return the first uppercase-letter+digits token that has a body spec."""
    body_dir = Path(specs_dir) / "body"
    if not body_dir.is_dir():
        return None

    known = {p.stem for p in body_dir.glob("*.spec")}
    for match in _TOKEN_RE.finditer(message):
        if match.group(0) in known:
            return match.group(0)
    return None
