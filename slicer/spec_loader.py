"""Plaintext spec file loader.

A spec file is a sequence of `field_name  length` lines. `#` starts a
comment (line-leading or trailing). Blank lines are ignored.

Arrays use a `@repeat <group> <count>` ... `@end` block:

    @repeat records 20
        break             4
        cifNumber        16
        mobileNumber     20
        customerStatus    2
    @end

Each iteration of the group consumes one copy of the inner fields and is
emitted by the parser as `group[NN].field` (1-indexed, two-digit). Nested
@repeat is not supported in v0.1.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScalarField:
    name: str
    length: int


@dataclass(frozen=True, slots=True)
class RepeatGroup:
    name: str
    count: int
    fields: tuple[ScalarField, ...]

    @property
    def length(self) -> int:
        """Total bytes consumed by all iterations of this group."""
        return self.count * sum(f.length for f in self.fields)


SpecItem = ScalarField | RepeatGroup
Spec = list[SpecItem]

# Back-compat alias for type hints from earlier versions.
SpecField = tuple[str, int]


def load_spec(path: str | Path) -> Spec:
    """Load a spec file and return ordered items (ScalarField or RepeatGroup).

    Raises FileNotFoundError if missing, and ValueError with file:line context
    for any malformed line.
    """
    spec_path = Path(path)
    if not spec_path.is_file():
        raise FileNotFoundError(f"spec not found: {spec_path}")

    items: Spec = []
    seen: set[str] = set()
    current_group: tuple[str, int, list[ScalarField]] | None = None  # (name, count, fields)

    for lineno, raw_line in enumerate(spec_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = _strip_comment(raw_line).strip()
        if not line:
            continue

        if line.startswith("@"):
            current_group = _handle_directive(line, lineno, spec_path, current_group, items, seen)
            continue

        scalar = _parse_field_line(line, lineno, spec_path, raw_line)

        if current_group is not None:
            inner_name = scalar.name
            inner_seen = {f.name for f in current_group[2]}
            if inner_name in inner_seen:
                raise ValueError(
                    f"{spec_path}:{lineno}: duplicate field {inner_name!r} in @repeat {current_group[0]!r}"
                )
            current_group[2].append(scalar)
        else:
            if scalar.name in seen:
                raise ValueError(f"{spec_path}:{lineno}: duplicate field name {scalar.name!r}")
            seen.add(scalar.name)
            items.append(scalar)

    if current_group is not None:
        raise ValueError(f"{spec_path}: unterminated @repeat {current_group[0]!r} (missing @end)")

    if not items:
        raise ValueError(f"{spec_path}: spec is empty")

    return items


def spec_total_length(spec: Spec) -> int:
    """Sum of all field lengths in the spec (including repeats)."""
    return sum(item.length for item in spec)


def spec_field_names(spec: Spec) -> list[str]:
    """Top-level field/group names — used by the dispatcher to find service_code."""
    return [item.name for item in spec]


def spec_field_count(spec: Spec) -> int:
    """Total number of parsed fields a spec will emit (expanding @repeat groups)."""
    return sum(
        item.count * len(item.fields) if isinstance(item, RepeatGroup) else 1 for item in spec
    )


# ---------------------------------------------------------------------------
# internals
# ---------------------------------------------------------------------------


def _strip_comment(line: str) -> str:
    idx = line.find("#")
    return line if idx == -1 else line[:idx]


def _looks_like_type_hint(token: str) -> bool:
    # Reserve these shapes for v0.2 typed validation.
    known_prefixes = ("numeric", "string", "date:", "enum:", "required")
    return any(token == p or token.startswith(p) for p in known_prefixes)


def _parse_field_line(line: str, lineno: int, path: Path, raw_line: str) -> ScalarField:
    parts = line.split()
    if len(parts) < 2:
        raise ValueError(f"{path}:{lineno}: expected '<name> <length>', got: {raw_line!r}")

    name, length_str, *extra = parts
    if extra and not _looks_like_type_hint(extra[0]):
        raise ValueError(f"{path}:{lineno}: unexpected token after length: {extra[0]!r}")

    try:
        length = int(length_str)
    except ValueError as exc:
        raise ValueError(f"{path}:{lineno}: length must be an integer, got {length_str!r}") from exc

    if length <= 0:
        raise ValueError(f"{path}:{lineno}: length must be positive, got {length}")

    return ScalarField(name=name, length=length)


def _handle_directive(
    line: str,
    lineno: int,
    path: Path,
    current_group: tuple[str, int, list[ScalarField]] | None,
    items: Spec,
    seen: set[str],
) -> tuple[str, int, list[ScalarField]] | None:
    parts = line.split()
    directive = parts[0]

    if directive == "@repeat":
        if current_group is not None:
            raise ValueError(f"{path}:{lineno}: nested @repeat is not supported")
        if len(parts) != 3:
            raise ValueError(f"{path}:{lineno}: expected '@repeat <name> <count>', got: {line!r}")
        _, group_name, count_str = parts
        try:
            count = int(count_str)
        except ValueError as exc:
            raise ValueError(
                f"{path}:{lineno}: @repeat count must be an integer, got {count_str!r}"
            ) from exc
        if count <= 0:
            raise ValueError(f"{path}:{lineno}: @repeat count must be positive, got {count}")
        if group_name in seen:
            raise ValueError(f"{path}:{lineno}: duplicate name {group_name!r}")
        seen.add(group_name)
        return (group_name, count, [])

    if directive == "@end":
        if current_group is None:
            raise ValueError(f"{path}:{lineno}: @end without matching @repeat")
        group_name, count, fields = current_group
        if not fields:
            raise ValueError(f"{path}:{lineno}: @repeat {group_name!r} has no fields")
        items.append(RepeatGroup(name=group_name, count=count, fields=tuple(fields)))
        return None

    raise ValueError(f"{path}:{lineno}: unknown directive {directive!r}")
