"""Rendering: table / json / raw / offset views of a ParseResult."""

from __future__ import annotations

import json
from io import StringIO

from rich.console import Console
from rich.table import Table

from slicer.models import ParseResult


def render_table(result: ParseResult, *, offsets: bool = False) -> str:
    """Pretty rich table. Returns the rendered string."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=False, width=120)

    if result.service_code:
        console.print(f"service_code: [bold]{result.service_code}[/bold]")
        console.print()

    table = Table(show_header=True, header_style="bold")
    if offsets:
        table.add_column("OFFSET", style="dim", no_wrap=True)
    table.add_column("FIELD", no_wrap=True)
    table.add_column("VALUE", overflow="fold")

    for f in result.fields:
        row = [f.name, f.value]
        if offsets:
            row.insert(0, f"{f.start}-{f.end}")
        table.add_row(*row)

    console.print(table)

    for warn in result.warnings:
        console.print(f"[yellow][WARN][/yellow] {warn}")
    for err in result.errors:
        console.print(f"[red][ERROR][/red] {err}")
    if result.unparsed_tail:
        console.print()
        console.print(f"[dim]unparsed_tail:[/dim] {result.unparsed_tail!r}")

    return buf.getvalue()


def render_json(result: ParseResult) -> str:
    """Canonical JSON form."""
    return json.dumps(result.as_dict(), indent=2, ensure_ascii=False)


def render_raw(result: ParseResult) -> str:
    """Flat `key=value` lines. One line per parsed field."""
    lines = [f"{f.name}={f.value}" for f in result.fields]
    return "\n".join(lines)
