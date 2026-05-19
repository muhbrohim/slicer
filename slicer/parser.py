"""Sequential offset slicer.

Pure function. No I/O. No globals. Reused for both header and body.
"""

from __future__ import annotations

from slicer.models import ParsedField
from slicer.spec_loader import RepeatGroup, ScalarField, Spec


def sequential_parse(
    message: str,
    spec: Spec,
    start_pos: int = 0,
) -> tuple[list[ParsedField], int, list[str]]:
    """Slice `message` according to `spec`, starting at `start_pos`.

    Returns:
        parsed: ParsedField list (up to the first truncation, if any).
        new_pos: position immediately after the last consumed byte.
        errors: list of error strings (e.g. truncation).
    """
    pos = start_pos
    parsed: list[ParsedField] = []
    errors: list[str] = []
    msg_len = len(message)

    for item in spec:
        if isinstance(item, ScalarField):
            new_pos, truncated = _slice_one(
                item.name, item.length, message, msg_len, pos, parsed, errors
            )
            pos = new_pos
            if truncated:
                return parsed, pos, errors
        elif isinstance(item, RepeatGroup):
            for i in range(item.count):
                prefix = f"{item.name}[{i + 1:02d}]"
                for inner in item.fields:
                    new_pos, truncated = _slice_one(
                        f"{prefix}.{inner.name}",
                        inner.length,
                        message,
                        msg_len,
                        pos,
                        parsed,
                        errors,
                    )
                    pos = new_pos
                    if truncated:
                        return parsed, pos, errors
        else:
            raise TypeError(f"unexpected spec item: {type(item).__name__}")

    return parsed, pos, errors


def _slice_one(
    name: str,
    length: int,
    message: str,
    msg_len: int,
    pos: int,
    parsed: list[ParsedField],
    errors: list[str],
) -> tuple[int, bool]:
    end = pos + length
    if end > msg_len:
        have = max(msg_len - pos, 0)
        errors.append(f"Message truncated at field {name!r} (need {length}, have {have})")
        return pos, True
    parsed.append(ParsedField(name=name, value=message[pos:end], start=pos, end=end - 1))
    return end, False
