"""Plaintext spec file loader.

A spec file is a sequence of `field_name  length` lines. `#` starts a comment
(line-leading or trailing). Blank lines are ignored. Returns the parsed fields
as an ordered list of `(name, length)` tuples.
"""

from __future__ import annotations

from pathlib import Path

SpecField = tuple[str, int]


def load_spec(path: str | Path) -> list[SpecField]:
    """Load a spec file and return ordered `(name, length)` tuples.

    Raises FileNotFoundError if the file does not exist, and ValueError with a
    file:line context string for any malformed line.
    """
    spec_path = Path(path)
    if not spec_path.is_file():
        raise FileNotFoundError(f"spec not found: {spec_path}")

    fields: list[SpecField] = []
    seen: set[str] = set()

    for lineno, raw_line in enumerate(spec_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = _strip_comment(raw_line).strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"{spec_path}:{lineno}: expected '<name> <length>', got: {raw_line!r}")

        name, length_str, *extra = parts
        # v0.1 ignores trailing type hints (planned for v0.2), but still
        # rejects garbage if the third token is not a known type-hint shape.
        if extra and not _looks_like_type_hint(extra[0]):
            raise ValueError(f"{spec_path}:{lineno}: unexpected token after length: {extra[0]!r}")

        try:
            length = int(length_str)
        except ValueError as exc:
            raise ValueError(
                f"{spec_path}:{lineno}: length must be an integer, got {length_str!r}"
            ) from exc

        if length <= 0:
            raise ValueError(f"{spec_path}:{lineno}: length must be positive, got {length}")

        if name in seen:
            raise ValueError(f"{spec_path}:{lineno}: duplicate field name {name!r}")
        seen.add(name)

        fields.append((name, length))

    if not fields:
        raise ValueError(f"{spec_path}: spec is empty")

    return fields


def spec_total_length(fields: list[SpecField]) -> int:
    """Sum of all field lengths."""
    return sum(length for _, length in fields)


def _strip_comment(line: str) -> str:
    idx = line.find("#")
    return line if idx == -1 else line[:idx]


def _looks_like_type_hint(token: str) -> bool:
    # Reserve these shapes for v0.2 typed validation.
    known_prefixes = ("numeric", "string", "date:", "enum:", "required")
    return any(token == p or token.startswith(p) for p in known_prefixes)
