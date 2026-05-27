"""Typer CLI: `slice` (parse) and `spec` (manage spec files)."""

from __future__ import annotations

import contextlib
import json
import os
import sys
from pathlib import Path

import typer
from rich.console import Console

from slicer import __version__
from slicer.dispatcher import parse_message
from slicer.endpoints import index_by_service_code, load_endpoints
from slicer.formatter import render_json, render_raw, render_table
from slicer.spec_loader import load_spec, spec_field_count, spec_total_length

# Rich uses Unicode box characters; ensure stdout/stderr can encode them on
# Windows consoles that default to cp1252.
for _stream in (sys.stdout, sys.stderr):
    reconfigure = getattr(_stream, "reconfigure", None)
    if callable(reconfigure):
        with contextlib.suppress(OSError, ValueError):
            reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# shared helpers
# ---------------------------------------------------------------------------

_console = Console()


def _resolve_specs_dir(override: Path | None) -> Path:
    if override is not None:
        return override.expanduser().resolve()
    env = os.environ.get("SLICER_HOME")
    if env:
        return (Path(env) / "specs").expanduser().resolve()
    return (Path.cwd() / "specs").resolve()


def _read_message(message: str | None) -> str:
    if message is not None:
        return message
    if not sys.stdin.isatty():
        return sys.stdin.read().rstrip("\r\n")
    _console.print("[dim]Paste message and press Enter:[/dim]")
    try:
        return input()
    except EOFError:
        return ""


# ---------------------------------------------------------------------------
# slice command
# ---------------------------------------------------------------------------


def slice_main(
    message: str | None = typer.Argument(
        None,
        help="Message to parse. If omitted, read from stdin (or interactive paste).",
    ),
    json_out: bool = typer.Option(False, "--json", help="Emit JSON."),
    raw: bool = typer.Option(False, "--raw", help="Emit key=value lines."),
    offsets: bool = typer.Option(False, "--offsets", help="Include offset column."),
    specs_dir: Path | None = typer.Option(
        None,
        "--specs-dir",
        help="Override the specs directory (default: $SLICER_HOME/specs or ./specs).",
    ),
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    """Parse a fixed-length message using your specs."""
    if version:
        typer.echo(__version__)
        raise typer.Exit()

    if json_out and raw:
        typer.echo("error: --json and --raw are mutually exclusive", err=True)
        raise typer.Exit(code=2)

    msg = _read_message(message)
    if not msg:
        typer.echo("error: no message provided", err=True)
        raise typer.Exit(code=2)

    result = parse_message(msg, _resolve_specs_dir(specs_dir))

    if json_out:
        typer.echo(render_json(result))
    elif raw:
        typer.echo(render_raw(result))
    else:
        sys.stdout.write(render_table(result, offsets=offsets))

    if result.errors:
        raise typer.Exit(code=1)


def slice_app() -> None:
    """Console-script entry point for `slice`."""
    typer.run(slice_main)


# ---------------------------------------------------------------------------
# spec app (multi-command)
# ---------------------------------------------------------------------------

spec_app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Manage slicer spec files (list / show / create).",
)


@spec_app.command("list")
def spec_list(
    specs_dir: Path | None = typer.Option(None, "--specs-dir"),
    json_out: bool = typer.Option(
        False, "--json", help="Emit a JSON array (one object per spec)."
    ),
) -> None:
    """List all body specs."""
    root = _resolve_specs_dir(specs_dir)
    body_dir = root / "body"
    if not body_dir.is_dir():
        typer.echo(f"error: no body spec directory at {body_dir}", err=True)
        raise typer.Exit(code=1)
    specs = sorted(body_dir.glob("*.spec"))
    if not specs:
        if json_out:
            typer.echo("[]")
        else:
            typer.echo("(no body specs found)")
        return

    # Load endpoint map once (tolerate missing file in dev environments).
    ep_index = {}
    try:
        ep_index = index_by_service_code(load_endpoints(root / "reff" / "endpoints.txt"))
    except FileNotFoundError:
        pass

    if json_out:
        rows: list[dict[str, object]] = []
        for path in specs:
            entry: dict[str, object] = {
                "service_code": path.stem,
                "spec_path": str(path),
            }
            try:
                spec = load_spec(path)
                entry["fields"] = spec_field_count(spec)
                entry["bytes"] = spec_total_length(spec)
                meta = getattr(spec, "metadata", {}) or {}
                entry["endpoint"] = (
                    None if meta.get("endpoint") in (None, "<none>") else meta["endpoint"]
                )
                entry["category"] = (
                    None if meta.get("category") in (None, "-") else meta["category"]
                )
                entry["section"] = (
                    None if meta.get("section") in (None, "-") else meta["section"]
                )
                entry["program"] = (
                    None if meta.get("program") in (None, "<none>") else meta["program"]
                )
            except (ValueError, FileNotFoundError) as exc:
                entry["error"] = str(exc)
                # Fall back to endpoint map by filename if loading failed.
                ep = ep_index.get(path.stem.lstrip("#").upper())
                if ep:
                    entry["endpoint"] = ep.url
                    entry["category"] = ep.category
                    entry["section"] = ep.section
            rows.append(entry)
        # Sort: real endpoints first (alphabetical), orphans last.
        rows.sort(key=lambda r: (r.get("endpoint") is None, r.get("endpoint") or "", r["service_code"]))
        typer.echo(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    for path in specs:
        try:
            fields = load_spec(path)
            count = spec_field_count(fields)
            total = spec_total_length(fields)
            meta = getattr(fields, "metadata", {}) or {}
            ep = meta.get("endpoint")
            ep_str = ep if ep and ep != "<none>" else "-"
            pgm = meta.get("program")
            pgm_str = pgm if pgm and pgm != "<none>" else "-"
            typer.echo(
                f"{path.stem:<12} {count:>4} fields  {total:>5} bytes   {pgm_str:<9}  {ep_str}"
            )
        except (ValueError, FileNotFoundError) as exc:
            typer.echo(f"{path.stem:<12} [invalid: {exc}]")


@spec_app.command("show")
def spec_show(
    name: str = typer.Argument(..., help="Service code (e.g. CA1017) or 'header'."),
    specs_dir: Path | None = typer.Option(None, "--specs-dir"),
) -> None:
    """Print the contents of a spec file."""
    root = _resolve_specs_dir(specs_dir)
    path = root / "header.spec" if name.lower() == "header" else root / "body" / f"{name}.spec"
    if not path.is_file():
        typer.echo(f"error: spec not found: {path}", err=True)
        raise typer.Exit(code=1)
    typer.echo(path.read_text(encoding="utf-8"))


@spec_app.command("create")
def spec_create(
    name: str = typer.Argument(..., help="Service code for the new body spec, e.g. CA2020."),
    specs_dir: Path | None = typer.Option(None, "--specs-dir"),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing spec."),
) -> None:
    """Create a new body spec from pasted 'field length' lines."""
    root = _resolve_specs_dir(specs_dir)
    body_dir = root / "body"
    body_dir.mkdir(parents=True, exist_ok=True)
    out = body_dir / f"{name}.spec"

    if out.exists() and not force:
        typer.echo(f"error: {out} already exists. Pass --force to overwrite.", err=True)
        raise typer.Exit(code=1)

    if sys.stdin.isatty():
        _console.print(
            f"[dim]Paste 'field length' lines for {name}, "
            f"then press Enter on a blank line to finish:[/dim]"
        )
        lines: list[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "":
                break
            lines.append(line)
        content = "\n".join(lines) + ("\n" if lines else "")
    else:
        content = sys.stdin.read()

    out.write_text(content, encoding="utf-8")

    # Validate immediately so the user knows the spec actually parses.
    try:
        fields = load_spec(out)
    except (ValueError, FileNotFoundError) as exc:
        typer.echo(f"warning: spec written but failed to parse: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(
        f"wrote {out} ({spec_field_count(fields)} fields, {spec_total_length(fields)} bytes)"
    )
