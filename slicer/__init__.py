"""slicer — spec-driven fixed-length message parser."""

__version__ = "0.1.0"

from slicer.dispatcher import parse_message
from slicer.endpoints import Endpoint, by_service_code, by_url, load_endpoints
from slicer.models import ParsedField, ParseResult
from slicer.parser import sequential_parse
from slicer.programs import Program, load_programs
from slicer.spec_loader import LoadedSpec, RepeatGroup, ScalarField, load_spec, spec_total_length

__all__ = [
    "Endpoint",
    "LoadedSpec",
    "ParseResult",
    "ParsedField",
    "Program",
    "RepeatGroup",
    "ScalarField",
    "__version__",
    "by_service_code",
    "by_url",
    "load_endpoints",
    "load_programs",
    "load_spec",
    "parse_message",
    "sequential_parse",
    "spec_total_length",
]
