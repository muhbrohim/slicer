# slicer

> Spec-driven fixed-length message parser for AS400 / DB2 / banking switch /
> legacy enterprise TCP payloads.

Replaces fragile Excel `MID()` workflows with maintainable, version-controlled
protocol definitions. Terminal-first, editor-native, zero configuration.

```
copy raw message  ->  slice  ->  parsed table in 1 second
```

---

## Why

Enterprise developers debug fixed-length protocols using Excel substring
formulas. That is error-prone, non-shareable, non-scriptable, and impossible
to grep, diff or audit. Slicer keeps each protocol as a plaintext `.spec`
file and provides one generic parser that consumes any spec.

See [`docs/DESIGN.txt`](docs/DESIGN.txt) for the full design document.

---

## Install

```powershell
git clone <repo>
cd slicer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

To make `slice` and `spec` available in every PowerShell window without
activation, add the venv's `Scripts` folder to your User PATH:

```powershell
$venvScripts = (Resolve-Path .\.venv\Scripts).Path
[Environment]::SetEnvironmentVariable(
    'Path',
    "$([Environment]::GetEnvironmentVariable('Path','User'));$venvScripts",
    'User'
)
[Environment]::SetEnvironmentVariable('SLICER_HOME', (Get-Location).Path, 'User')
```

Open a new PowerShell window and the two CLI entry points are on PATH:

| command | purpose                       |
|---------|-------------------------------|
| `slice` | parse a single message        |
| `spec`  | list / show / create specs    |

Requires Python 3.10+.

---

## Quickstart — real example

The repository ships with a real production payload at
`sample_messages/us1003_real.txt` and the matching specs:

- `specs/header.spec` — 220-byte DSVI-HDR-INFO TCP envelope.
- `specs/body/#US1003.spec` — response prefix + echo block + 20-element
  customer array + `#LOC` terminator.

Parse it:

```powershell
slice "$(Get-Content $env:SLICER_HOME\sample_messages\us1003_real.txt -Raw)"
```

You'll see the TCP header fields (`HDR_TAG=ADSVADSV`, `service_code=#US1003`,
`HDR_DATA_LEN=00953`, ...), the response prefix (`resp_code=06`, `key_type=G`,
`key_bank=1327`), the echo block, and twenty fully-parsed customer records.

Switch to JSON to get the array as a real list:

```powershell
slice "$(Get-Content $env:SLICER_HOME\sample_messages\us1003_real.txt -Raw)" --json
```

```json
{
  "service_code": "#US1003",
  "header": { "HDR_TAG": "ADSVADSV", "service_code": "#US1003", ... },
  "body": {
    "resp_code": "06",
    "key_type": "G",
    "key_bank": "1327",
    "records": [
      { "break": "=01=", "cifNumber": "WL_0001         ", "mobileNumber": "0909809898          ", "customerStatus": "1 " },
      { "break": "=02=", "cifNumber": "0000000000000001", ... },
      ...
    ],
    "loc_end": "#LOC"
  }
}
```

---

## CLI

### `slice`

```powershell
slice                       # interactive: paste, then press Enter
slice "MESSAGE..."          # positional argument
Get-Content msg.txt | slice # stdin
Get-Clipboard | slice       # clipboard

slice $msg --json           # nested JSON
slice $msg --raw            # flat key=value lines
slice $msg --offsets        # add start-end column
slice $msg --specs-dir D:\other\specs   # override specs directory
```

Default specs directory is `$env:SLICER_HOME\specs`, falling back to `.\specs`.

### `spec`

```powershell
spec list                   # show all body specs (field count + bytes)
spec show header            # print the header spec
spec show '#US1003'         # print one body spec (quote names with #)
spec create CA9000          # paste field-length lines, blank Enter to save
```

---

## Spec format

One field per line, name then length. Comments start with `#`. Blank lines
are ignored.

```
# header section
HDR_TAG               8
HDR_SERVICE_TYPE      1
service_code          7
HDR_CLIENT_ID        20
```

**Required:** the header spec must define a field literally named
`service_code`. The dispatcher uses its value to load
`specs/body/{service_code}.spec` (`#`, alphanumerics — anything legal as a
Windows filename is fine).

### Arrays — `@repeat ... @end`

For protocols with a fixed-count repeating block, use a `@repeat` directive:

```
# echo block (scalars)
echo_cifNumber       16
echo_uid             20

# 20 customer records, 42 bytes each
@repeat records 20
    break             4
    cifNumber        16
    mobileNumber     20
    customerStatus    2
@end

loc_end               4
```

The parser emits each record's fields as `records[01].break`,
`records[01].cifNumber`, ... `records[20].customerStatus`. JSON output
collapses them into a real array under `records`.

Nested `@repeat` is not supported in v0.1.

### Planned for v0.2 — typed fields

The loader already accepts forward-compatible type hints (parsed but ignored
in v0.1):

```
amount    13   numeric
date       8   date:YYYYMMDD
status     2   enum:OK,KO,PD
name      30   string:required
```

---

## Neovim integration

A thin Lua wrapper lives at [`nvim/slicer.lua`](nvim/slicer.lua).

```
<leader>sp    slice the current line
<leader>ss    slice the visual selection
<leader>so    open the spec whose service code appears on the current line
```

Set `SLICER_HOME` so the plugin can find your specs:

```lua
vim.env.SLICER_HOME = "C:/Users/you/personal/slicer"
require("slicer").setup()
```

---

## Error handling

Slicer never crashes on malformed input. Instead it returns a result with
warnings/errors plus whatever was parsed successfully:

| situation                      | behavior                                  |
|--------------------------------|-------------------------------------------|
| missing `header.spec`          | error, empty result                       |
| header missing `service_code`  | error, header-only result                 |
| missing body spec              | warning, header parsed, body as raw tail  |
| message truncated mid-field    | error, return fields parsed so far        |
| message longer than spec       | warning, expose `unparsed_tail`           |
| invalid spec syntax            | `ValueError` with file:line context       |

CLI exit code is `0` on a clean parse, `1` when errors were recorded, `2`
on bad invocation.

---

## Tests

```powershell
pytest -q
```

39 cases across `test_parser.py`, `test_spec_loader.py`, `test_dispatcher.py`.
CI runs Windows on Python 3.10–3.12. See
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## Roadmap

```
v0.1   sequential parser, dispatcher, CLI, Neovim, @repeat arrays  (current)
v0.2   typed validation (numeric / required / date / enum)
v0.3   `spec validate` linter
v0.4   hex view and binary mode
v0.5   message diff viewer
v0.6   Textual TUI mode
v0.7   message builder
v0.8   request / response correlation
v0.9   TCP replay
v1.0   spec versioning + multi-version dispatch
```

Full roadmap and design rationale in [`docs/DESIGN.txt`](docs/DESIGN.txt).

---

## License

MIT — see [`LICENSE`](LICENSE).
