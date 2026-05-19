"""Generate body .spec files from the reference markdown.

Reads  specs/reff/all-spec.md , walks each CTBCLH## section, extracts the
Response Message TCP Body fields, and writes  specs/body/{service_code}.spec .

Each generated spec begins with the standard 26-byte response prefix
(resp_code + key_type + key_bank + key_val).  The body fields follow as
written in the reference (sanitized to valid spec field names).  Repeating
blocks marked with "N records" / "<groupName>" in the table become
`@repeat groupName N ... @end` blocks.

Run from the project root:
    python scripts/generate_specs.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = ROOT / "specs" / "reff" / "all-spec.md"
OUTPUT_DIR = ROOT / "specs" / "body"

# Hand-written specs to leave alone.
SKIP_SERVICE_CODES = {"#US1003", "#CA1030", "ANI6000", "#CA1033"}

RESPONSE_PREFIX = """\
# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL
"""


@dataclass
class Field:
    name: str
    length: int
    required: str
    fmt: str
    remark: str
    array_count: int | None = None
    array_name: str | None = None


def split_row(line: str) -> list[str]:
    """Split a markdown table row into cell values."""
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def is_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-+:?", c) for c in cells if c)


def sanitize_name(raw: str) -> str:
    """Convert raw field-name text to a valid spec field identifier."""
    raw = raw.strip()
    # Strip a leading numeric prefix like "1.0 "
    raw = re.sub(r"^\d+(?:\.\d+)?\s+", "", raw)
    # Replace any non-alphanumeric with _
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", raw)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if cleaned and cleaned[0].isdigit():
        cleaned = "f_" + cleaned
    return cleaned


def parse_length(s: str) -> int | None:
    """Parse a length cell. '16' -> 16, '13.2' -> 13, '-' -> None, '' -> None."""
    s = (s or "").strip()
    if not s or s == "-":
        return None
    m = re.match(r"^(\d+)(?:\.\d+)?$", s)
    if m:
        return int(m.group(1))
    return None


def parse_catalog(lines: list[str]) -> dict[str, str]:
    """Build CTBCLH## -> service code mapping from the Services Catalog table."""
    catalog: dict[str, str] = {}
    in_section = False
    for line in lines:
        if line.startswith("## Services Catalog"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        cells = split_row(line)
        if is_separator(cells):
            continue
        if len(cells) < 7 or cells[0] == "No":
            continue
        # Columns: No | API Name | FSD | GROUP | SRV_CODE | CLIENT_ID | API ID | ...
        srv_code = cells[4]
        api_id = cells[6]
        if api_id.startswith("CTBCLH") and srv_code:
            catalog[api_id] = srv_code
    return catalog


def find_section(api_id: str, lines: list[str]) -> list[str] | None:
    """Return the lines belonging to ## <api_id> ... up to the next ## heading."""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {api_id}":
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return lines[start:end]


def detect_header_columns(header_cells: list[str]) -> dict[str, int]:
    """Return mapping of role -> column index for a field-table header row."""
    cols: dict[str, int] = {}
    for i, c in enumerate(header_cells):
        cl = c.strip()
        if cl == "Field Name" and "name" not in cols:
            cols["name"] = i
        elif cl == "Required" and "required" not in cols:
            cols["required"] = i
        elif cl == "Format" and "format" not in cols:
            cols["format"] = i
        elif cl == "ASC":  # ASC byte length — preferred when both ASC/FSD present
            cols["length"] = i
        elif cl == "Length" and "length" not in cols:
            cols["length"] = i
        elif cl == "FSD" and "length" not in cols:
            cols["length"] = i
        elif cl == "Remark" and "remark" not in cols:
            cols["remark"] = i
    return cols


def extract_response_fields(section: list[str]) -> list[Field]:
    """Find Response Message → TCP Message Body field table and extract rows."""
    # Locate every field-header row ("| ... Field Name ... |") in the section.
    header_rows: list[int] = [
        i for i, line in enumerate(section)
        if line.startswith("|") and "Field Name" in line
    ]
    if not header_rows:
        return []

    # Find an explicit "Response Message" marker if it exists.
    resp_idx = None
    for i, line in enumerate(section):
        if line.startswith("| Response Message"):
            resp_idx = i
            break

    if resp_idx is not None:
        # First header row after the Response marker
        header_idx = next((h for h in header_rows if h > resp_idx), None)
    else:
        # No explicit marker. If the section has two header rows (request + response),
        # use the second one; if only one, use it.
        header_idx = header_rows[1] if len(header_rows) >= 2 else header_rows[0]

    if header_idx is None:
        return []

    header_cells = split_row(section[header_idx])
    cols = detect_header_columns(header_cells)
    if "name" not in cols or "length" not in cols:
        return []

    # Iterate body rows.
    fields: list[Field] = []
    in_body = False
    seen_names: dict[str, int] = {}
    pending_array_count: int | None = None
    pending_array_name: str | None = None

    for i in range(header_idx + 1, len(section)):
        line = section[i]
        if not line.startswith("|"):
            break
        cells = split_row(line)
        if is_separator(cells):
            continue
        if not cells:
            continue
        first = cells[0].strip() if cells else ""

        # Section markers
        if first == "TCP Message Body":
            in_body = True
            continue
        if first == "TCP Message Header":
            in_body = False
            continue
        # Stop at next "Request Message" / "Response Message" header (shouldn't happen
        # within response, but safety net)
        if first in ("Request Message", "Response Message"):
            break

        if not in_body:
            continue

        # Skip all-blank rows
        if all(not c for c in cells):
            continue

        # Skip duplicated column-header rows (some sections repeat them)
        if cells[cols["name"]].strip() == "Field Name" if cols["name"] < len(cells) else False:
            continue

        raw_name = cells[cols["name"]].strip() if cols["name"] < len(cells) else ""
        if not raw_name:
            continue

        length_str = cells[cols["length"]].strip() if cols["length"] < len(cells) else ""
        length = parse_length(length_str)
        # If "length" is ASC but blank/dash, fall back to a later "Length" or "FSD" column
        if length is None:
            for j in range(cols["length"] + 1, len(cells)):
                cand = parse_length(cells[j])
                if cand is not None:
                    length = cand
                    break
        if length is None or length <= 0:
            continue

        name = sanitize_name(raw_name)
        if not name:
            continue
        # Deduplicate names within the spec (some specs reuse generic names like
        # "addressLine1" for home/work/legal/correspondence addresses).
        count = seen_names.get(name, 0)
        seen_names[name] = count + 1
        if count > 0:
            name = f"{name}_{count + 1}"

        required = cells[cols["required"]].strip() if "required" in cols and cols["required"] < len(cells) else ""
        fmt = cells[cols["format"]].strip() if "format" in cols and cols["format"] < len(cells) else ""
        remark = cells[cols["remark"]].strip() if "remark" in cols and cols["remark"] < len(cells) else ""

        # Detect array marker. Look at trailing cells (past the remark column) for
        # an "N records" pattern; the next non-empty cell is the group name.
        array_count = None
        array_name = None
        scan_from = (cols.get("remark") or cols["length"]) + 1
        record_re = re.compile(r"^(\d+)\s+records?$", re.IGNORECASE)
        for j in range(scan_from, len(cells)):
            c = cells[j].strip()
            if not c:
                continue
            m = record_re.match(c)
            if m and array_count is None:
                array_count = int(m.group(1))
                continue
            if array_count is not None and array_name is None:
                array_name = sanitize_name(c)

        if array_count and array_name:
            pending_array_count = array_count
            pending_array_name = array_name
            fields.append(
                Field(
                    name=name,
                    length=length,
                    required=required,
                    fmt=fmt,
                    remark=remark,
                    array_count=array_count,
                    array_name=array_name,
                )
            )
        else:
            fields.append(
                Field(name=name, length=length, required=required, fmt=fmt, remark=remark)
            )

    return fields


def render_spec(api_id: str, srv_code: str, fields: list[Field]) -> str:
    """Render a .spec file as text."""
    out: list[str] = []
    out.append(f"# {srv_code} - generated from {api_id} (specs/reff/all-spec.md).")
    out.append("# Layout: response prefix, then service body.")
    out.append("# Review and adjust array boundaries / field types as needed.")
    out.append("")
    out.append(RESPONSE_PREFIX.rstrip())
    out.append("")
    out.append("# --- service body")

    # Group fields by array. Once an array starts, every subsequent field with the
    # same array_name belongs to it; the array ends when a non-array field appears
    # or the field list ends.
    i = 0
    while i < len(fields):
        f = fields[i]
        if f.array_count and f.array_name:
            group_name = f.array_name
            count = f.array_count
            # Collect this and all subsequent fields up to the next array start (if any)
            group_fields: list[Field] = [f]
            j = i + 1
            while j < len(fields):
                nf = fields[j]
                if nf.array_count and nf.array_name and nf.array_name != group_name:
                    break
                group_fields.append(nf)
                j += 1
            out.append("")
            out.append(f"@repeat {group_name} {count}")
            for gf in group_fields:
                out.append(_format_line(gf, indent=4))
            out.append("@end")
            i = j
        else:
            out.append(_format_line(f, indent=0))
            i += 1

    out.append("")
    return "\n".join(out) + "\n"


def _format_line(f: Field, *, indent: int) -> str:
    pad = " " * indent
    name_width = 30
    name = f.name  # never truncate — names must remain unique
    spacer = " " * max(1, name_width - len(name))
    length_field = f"{f.length:>4}"
    bits = []
    if f.required:
        bits.append(f.required)
    if f.fmt:
        bits.append(f.fmt)
    tag = " ".join(bits)
    comment = ""
    if tag or f.remark:
        comment_bits = []
        if tag:
            comment_bits.append(tag)
        if f.remark:
            r = f.remark.replace("\n", " ").strip()
            if len(r) > 80:
                r = r[:77] + "..."
            comment_bits.append(r)
        comment = "    # " + "  ".join(comment_bits)
    return f"{pad}{name}{spacer}{length_field}{comment}"


def main() -> None:
    doc = DOC_PATH.read_text(encoding="utf-8")
    lines = doc.splitlines()

    catalog = parse_catalog(lines)
    print(f"Found {len(catalog)} services in catalog.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    skipped: list[tuple[str, str, str]] = []

    for api_id, srv_code in catalog.items():
        if srv_code in SKIP_SERVICE_CODES:
            skipped.append((api_id, srv_code, "hand-written, skipped"))
            continue
        section = find_section(api_id, lines)
        if section is None:
            skipped.append((api_id, srv_code, "section not found"))
            continue
        fields = extract_response_fields(section)
        if not fields:
            skipped.append((api_id, srv_code, "no response fields"))
            continue
        spec_text = render_spec(api_id, srv_code, fields)
        out_path = OUTPUT_DIR / f"{srv_code}.spec"
        out_path.write_text(spec_text, encoding="utf-8")
        generated.append((api_id, srv_code, len(fields)))

    print(f"\nGenerated {len(generated)} specs:")
    for api_id, srv_code, n in generated:
        print(f"  {api_id:>10}  ->  {srv_code:<10}  ({n} fields)")
    if skipped:
        print(f"\nSkipped {len(skipped)}:")
        for api_id, srv_code, reason in skipped:
            print(f"  {api_id:>10}  ->  {srv_code:<10}  ({reason})")


if __name__ == "__main__":
    main()
