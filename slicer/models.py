"""Data models used across the slicer pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field


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
            "header": {f.name: f.value for f in self.header},
            "body": {f.name: f.value for f in self.body},
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "unparsed_tail": self.unparsed_tail,
        }
