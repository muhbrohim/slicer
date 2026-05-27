"""Backfill structured metadata headers into all spec files.

Prepends (or refreshes) a 4-line block at the top of every
`specs/body/*.spec` and `specs/header.spec`:

    # service-code: #CA1017
    # endpoint:     /card/cash-transaction-add
    # category:     CA
    # section:      3.9

Idempotent: re-running the script removes any existing structured block first,
then re-emits it from the current endpoints map. Free-form prose comments
that follow are preserved.

Usage:
    python scripts/backfill_spec_headers.py              # dry run (default)
    python scripts/backfill_spec_headers.py --write      # actually mutate
    python scripts/backfill_spec_headers.py --specs-dir <path> --write
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from slicer.endpoints import Endpoint, index_by_service_code, load_endpoints  # noqa: E402
from slicer.programs import (  # noqa: E402
    Program,
    index_by_service_code as index_programs_by_service_code,
    load_programs,
)

# Keys we own at the top of every spec. Any leading `# key: value` line whose
# key is in this set is considered ours and will be stripped before re-emit.
OWNED_KEYS = ("service-code", "endpoint", "category", "section", "program")
_OWNED_RE = re.compile(rf"^\s*#\s*(?:{'|'.join(OWNED_KEYS)})\s*:.*$", re.IGNORECASE)


@dataclass
class Outcome:
    path: Path
    status: str  # "updated" | "unchanged" | "orphan-updated" | "orphan-unchanged"
    service_code: str | None
    endpoint: str | None


def derive_service_code(spec_path: Path) -> str:
    """Stem preserves the leading `#` already (it's part of the filename)."""
    return spec_path.stem


def strip_owned_metadata(lines: list[str]) -> list[str]:
    """Remove any leading owned-key metadata lines plus an immediately
    following bare-`#` separator line (the one we always emit)."""
    out = list(lines)
    while out and (_OWNED_RE.match(out[0]) or out[0].strip() == ""):
        # Only strip a blank line if it's directly between owned-keys and
        # later content. We handle blanks at the top conservatively: drop
        # one blank line only if the next line is also owned metadata.
        if out[0].strip() == "":
            if len(out) >= 2 and _OWNED_RE.match(out[1]):
                out.pop(0)
                continue
            break
        out.pop(0)
    # If the next line is a bare `#` separator we emitted, drop it too.
    if out and out[0].strip() == "#":
        out.pop(0)
    return out


def build_header(service_code: str, ep: Endpoint | None, pgm: Program | None) -> list[str]:
    url = ep.url if ep else "<none>"
    category = ep.category if ep else "-"
    section = ep.section if ep else "-"
    program = pgm.name if pgm else "<none>"
    return [
        f"# service-code: {service_code}",
        f"# endpoint:     {url}",
        f"# category:     {category}",
        f"# section:      {section}",
        f"# program:      {program}",
        "#",
    ]


def process_spec(
    spec_path: Path,
    ep_index: dict[str, Endpoint],
    pgm_index: dict[str, Program] | None = None,
    *,
    is_header: bool = False,
) -> tuple[Outcome, str]:
    pgm_index = pgm_index or {}
    original = spec_path.read_text(encoding="utf-8")
    raw_lines = original.splitlines()

    if is_header:
        # header.spec has no service code of its own.
        service_code = "<header>"
        ep = None
        pgm = None
    else:
        service_code = derive_service_code(spec_path)
        key = service_code.lstrip("#").upper()
        ep = ep_index.get(key)
        pgm = pgm_index.get(key)

    body_lines = strip_owned_metadata(raw_lines)
    header_lines = build_header(service_code, ep, pgm)
    new_lines = header_lines + body_lines

    # Preserve trailing newline if original had one.
    trailing = "\n" if original.endswith("\n") else ""
    new_content = "\n".join(new_lines) + trailing

    if new_content == original:
        status = "unchanged" if (ep or is_header) else "orphan-unchanged"
    else:
        status = "updated" if (ep or is_header) else "orphan-updated"

    return (
        Outcome(
            path=spec_path,
            status=status,
            service_code=None if is_header else service_code,
            endpoint=ep.url if ep else None,
        ),
        new_content,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--specs-dir", type=Path, default=ROOT / "specs")
    ap.add_argument("--endpoints", type=Path, default=None,
                    help="Path to endpoints.txt (default: <specs-dir>/reff/endpoints.txt)")
    ap.add_argument("--write", action="store_true",
                    help="Actually write changes (default is dry-run).")
    args = ap.parse_args()

    specs_dir: Path = args.specs_dir.resolve()
    endpoints_path = args.endpoints or (specs_dir / "reff" / "endpoints.txt")
    endpoints = load_endpoints(endpoints_path)
    ep_index = index_by_service_code(endpoints)

    programs_path = specs_dir / "reff" / "pgm-list.tsv"
    pgm_index: dict[str, Program] = {}
    if programs_path.is_file():
        pgm_index = index_programs_by_service_code(load_programs(programs_path))
    else:
        print(f"note: programs file not found at {programs_path} — `# program:` lines will be <none>")

    targets: list[tuple[Path, bool]] = []
    header_spec = specs_dir / "header.spec"
    if header_spec.is_file():
        targets.append((header_spec, True))
    body_dir = specs_dir / "body"
    for p in sorted(body_dir.glob("*.spec")):
        targets.append((p, False))

    outcomes: list[Outcome] = []
    for path, is_header in targets:
        outcome, new_content = process_spec(path, ep_index, pgm_index, is_header=is_header)
        outcomes.append(outcome)
        if args.write and outcome.status.endswith("updated"):
            path.write_text(new_content, encoding="utf-8")

    # Summary
    counts = {"updated": 0, "unchanged": 0, "orphan-updated": 0, "orphan-unchanged": 0}
    orphans: list[Outcome] = []
    for o in outcomes:
        counts[o.status] += 1
        if o.status.startswith("orphan"):
            orphans.append(o)

    print(f"Processed {len(outcomes)} spec file(s) under {specs_dir}")
    print(f"  updated:           {counts['updated']}")
    print(f"  unchanged:         {counts['unchanged']}")
    print(f"  orphan (updated):  {counts['orphan-updated']}")
    print(f"  orphan (no-op):    {counts['orphan-unchanged']}")
    if orphans:
        print()
        print("Orphan specs (no endpoint mapping):")
        for o in orphans:
            print(f"  {o.service_code}  ({o.path.name})")
    if not args.write:
        print()
        print("(dry-run) re-run with --write to apply changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
