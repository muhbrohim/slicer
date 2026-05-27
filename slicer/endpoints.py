"""Loader for the endpoint -> service-code mapping.

Source file format (`specs/reff/endpoints.txt`):

    # comment / blank lines are ignored
    /card/cash-transaction-add    3.9    CA    #CA1017

Four whitespace-separated columns: url, section, category, service_code.
Service codes may carry a leading `#` (matching the spec filename convention)
or be bare (e.g. ANI codes). Lookups are tolerant of the `#` prefix.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Endpoint:
    url: str
    section: str
    category: str
    service_code: str  # preserved as-written (with or without leading '#')


def default_endpoints_path() -> Path:
    """Resolve the canonical endpoints file location."""
    env = os.environ.get("SLICER_HOME")
    if env:
        candidate = Path(env) / "specs" / "reff" / "endpoints.txt"
        if candidate.is_file():
            return candidate
    return (Path.cwd() / "specs" / "reff" / "endpoints.txt").resolve()


def load_endpoints(path: str | Path | None = None) -> list[Endpoint]:
    """Parse the endpoints file. Skips blank lines and `#` comments."""
    p = Path(path) if path is not None else default_endpoints_path()
    if not p.is_file():
        raise FileNotFoundError(f"endpoints file not found: {p}")

    out: list[Endpoint] = []
    for lineno, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 4:
            raise ValueError(
                f"{p}:{lineno}: expected 4 columns (url section category service_code), got {len(parts)}: {raw!r}"
            )
        url, section, category, service_code = parts
        out.append(
            Endpoint(url=url, section=section, category=category, service_code=service_code)
        )
    return out


def _normalize(code: str) -> str:
    return code.lstrip("#").upper() if code else ""


def by_service_code(code: str, endpoints: list[Endpoint]) -> Endpoint | None:
    """Find an endpoint by service code. Tolerant of leading `#` and case."""
    target = _normalize(code)
    if not target:
        return None
    for ep in endpoints:
        if _normalize(ep.service_code) == target:
            return ep
    return None


def by_url(url: str, endpoints: list[Endpoint]) -> Endpoint | None:
    """Find an endpoint by URL path. Case-sensitive, exact match."""
    for ep in endpoints:
        if ep.url == url:
            return ep
    return None


def index_by_service_code(endpoints: list[Endpoint]) -> dict[str, Endpoint]:
    """Map normalized service code -> Endpoint for O(1) lookup."""
    return {_normalize(ep.service_code): ep for ep in endpoints}
