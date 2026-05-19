"""slicer — spec-driven fixed-length message parser."""

__version__ = "0.1.0"

from slicer.dispatcher import parse_message
from slicer.models import ParsedField, ParseResult
from slicer.parser import sequential_parse
from slicer.spec_loader import RepeatGroup, ScalarField, load_spec, spec_total_length

__all__ = [
    "ParseResult",
    "ParsedField",
    "RepeatGroup",
    "ScalarField",
    "__version__",
    "load_spec",
    "parse_message",
    "sequential_parse",
    "spec_total_length",
]
