"""Loader for the service-code -> program (LH/SC backend module) mapping.

Source file format (`specs/reff/pgm-list.tsv`), tab-separated, 8 columns:

    service_code <TAB> description <TAB> program_name <TAB> flag <TAB>
        active <TAB> last_changed <TAB> timestamp <TAB> user

Lines starting with `#` ARE data lines (service codes start with `#`).
Truly-blank lines are skipped. We use tab as the field separator, not
whitespace, so the description column may contain spaces freely.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Program:
    service_code: str   # preserved as-written (with leading '#' when present)
    description: str
    name: str           # e.g. "LHBSC10S"
    flag: str
    active: str
    last_changed: str
    timestamp: str
    user: str


def default_programs_path() -> Path:
    """Resolve the canonical programs file location."""
    env = os.environ.get("SLICER_HOME")
    if env:
        candidate = Path(env) / "specs" / "reff" / "pgm-list.tsv"
        if candidate.is_file():
            return candidate
    return (Path.cwd() / "specs" / "reff" / "pgm-list.tsv").resolve()


def load_programs(path: str | Path | None = None) -> list[Program]:
    """Parse the programs TSV. Skips blank lines."""
    p = Path(path) if path is not None else default_programs_path()
    if not p.is_file():
        raise FileNotFoundError(f"programs file not found: {p}")

    out: list[Program] = []
    for lineno, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) != 8:
            raise ValueError(
                f"{p}:{lineno}: expected 8 tab-separated columns, got {len(parts)}: {raw!r}"
            )
        out.append(
            Program(
                service_code=parts[0].strip(),
                description=parts[1].strip(),
                name=parts[2].strip(),
                flag=parts[3].strip(),
                active=parts[4].strip(),
                last_changed=parts[5].strip(),
                timestamp=parts[6].strip(),
                user=parts[7].strip(),
            )
        )
    return out


def _normalize(code: str) -> str:
    return code.lstrip("#").upper() if code else ""


def by_service_code(code: str, programs: list[Program]) -> Program | None:
    """Find a program by service code. Tolerant of leading `#` and case."""
    target = _normalize(code)
    if not target:
        return None
    for pgm in programs:
        if _normalize(pgm.service_code) == target:
            return pgm
    return None


def index_by_service_code(programs: list[Program]) -> dict[str, Program]:
    """Map normalized service code -> Program. First occurrence wins on dupes."""
    out: dict[str, Program] = {}
    for pgm in programs:
        key = _normalize(pgm.service_code)
        out.setdefault(key, pgm)
    return out
