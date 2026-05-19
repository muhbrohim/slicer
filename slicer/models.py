"""Data models used across the slicer pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_ARRAY_NAME_RE = re.compile(r"^(?P<group>[A-Za-z_][\w]*)\[(?P<idx>\d+)\]\.(?P<field>.+)$")


@dataclass(frozen=True, slots=True)
class ParsedField:
    """One slice of a message: name, value, and inclusive byte offsets."""

    name: str
    value: str
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "value": self.value,
            "start": self.start,
            "end": self.end,
        }


@dataclass(slots=True)
class ParseResult:
    """Full parse output: header + body + diagnostics."""

    service_code: str | None = None
    header: list[ParsedField] = field(default_factory=list)
    body: list[ParsedField] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    unparsed_tail: str | None = None

    @property
    def fields(self) -> list[ParsedField]:
        return [*self.header, *self.body]

    def as_dict(self) -> dict[str, object]:
        return {
            "service_code": self.service_code,
            "header": _build_nested(self.header),
            "body": _build_nested(self.body),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "unparsed_tail": self.unparsed_tail,
        }


def _build_nested(fields: list[ParsedField]) -> dict[str, object]:
    """Convert a flat ParsedField list into a dict, building arrays from
    `group[NN].field` names. Scalars stay at the top level."""
    out: dict[str, object] = {}
    arrays: dict[str, list[dict[str, str]]] = {}

    for f in fields:
        m = _ARRAY_NAME_RE.match(f.name)
        if m is None:
            out[f.name] = f.value
            continue
        group = m.group("group")
        idx = int(m.group("idx"))
        inner = m.group("field")
        bucket = arrays.setdefault(group, [])
        while len(bucket) < idx:
            bucket.append({})
        bucket[idx - 1][inner] = f.value

    for group, bucket in arrays.items():
        out[group] = bucket

    return out
