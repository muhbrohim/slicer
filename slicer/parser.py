"""Sequential offset slicer.

Pure function. No I/O. No globals. Reused for both header and body.
"""

from __future__ import annotations

from slicer.models import ParsedField
from slicer.spec_loader import SpecField


def sequential_parse(
    message: str,
    fields: list[SpecField],
    start_pos: int = 0,
) -> tuple[list[ParsedField], int, list[str]]:
    """Slice `message` according to `fields`, starting at `start_pos`.

    Returns:
        parsed: ParsedField list (up to the first truncation, if any).
        new_pos: position immediately after the last consumed byte.
        errors: list of error strings (e.g. truncation).
    """
    pos = start_pos
    parsed: list[ParsedField] = []
    errors: list[str] = []
    msg_len = len(message)

    for name, length in fields:
        end = pos + length
        if end > msg_len:
            have = max(msg_len - pos, 0)
            errors.append(f"Message truncated at field {name!r} (need {length}, have {have})")
            break

        value = message[pos:end]
        parsed.append(ParsedField(name=name, value=value, start=pos, end=end - 1))
        pos = end

    return parsed, pos, errors
