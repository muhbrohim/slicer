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

```bash
# from source
git clone <repo>
cd slicer
python -m pip install -e ".[dev]"
```

Two CLI entry points are installed:

| command | purpose                       |
|---------|-------------------------------|
| `slice` | parse a single message        |
| `spec`  | list / show / create specs    |

Requires Python 3.10+.

---

## Quickstart

1. Define a shared header at `specs/header.spec`:

   ```
   prefix          4
   channel         8
   service_code    6
   device         20
   ```

2. Define a body per API at `specs/body/CA1017.spec`:

   ```
   transaction_id   12
   amount           13
   response_code     2
   customer_name    30
   ```

3. Parse a message:

   ```bash
   slice "$(Get-Content sample_messages/ca1017_demo.txt)"
   ```

   Output (default rich table):

   ```
   service_code: CA1017

   FIELD              VALUE
   ----------------------------------------------------
   prefix             ADSV
   channel            MOBILE
   service_code       CA1017
   device             DEVICE-001-ABCDEFGH
   transaction_id     TRX000000001
   amount             0000000001350
   response_code      00
   customer_name      JOHN DOE
   ```

---

## CLI

### `slice`

```bash
slice                       # interactive paste (Ctrl-Z + Enter on Windows, Ctrl-D on *nix)
slice "MESSAGE..."          # positional
cat msg.txt   | slice       # stdin (bash)
Get-Content msg.txt | slice # stdin (PowerShell)

slice --json                # JSON output
slice --raw                 # key=value output
slice --offsets             # include start-end column
```

Combine with `--specs-dir DIR` to point at a non-default specs directory
(default is `$SLICER_HOME/specs` or `./specs`).

### `spec`

```bash
spec list                   # list all body specs
spec show CA1017            # print one spec
spec create CA2020          # paste "field length" lines, Ctrl-Z + Enter to save
```

---

## Neovim integration

A thin Lua wrapper lives at [`nvim/slicer.lua`](nvim/slicer.lua).

```
<leader>sp    slice the current line
<leader>ss    slice the visual selection
<leader>so    open the spec matching CA#### on the current line
```

Set `SLICER_HOME` so the plugin can find your specs:

```lua
vim.env.SLICER_HOME = "/path/to/slicer"
require("slicer").setup()
```

---

## Spec format

One field per line, name then length. Comments start with `#`. Blank lines
are ignored.

```
# customer header section
cif       10
name      30
amount    13   # trailing comment also allowed
```

The header spec **must** define a field named `service_code`. The dispatcher
uses its value to load the matching body spec from `specs/body/{code}.spec`.

Planned in v0.2: type hints like `amount 13 numeric`, `date 8 date:YYYYMMDD`,
`status 2 enum:OK,KO,PD`.

---

## Error handling

Slicer never crashes on malformed input. Instead it returns a result with
warnings/errors and whatever was parsed successfully:

| situation                      | behavior                                  |
|--------------------------------|-------------------------------------------|
| missing `header.spec`          | error, empty result                       |
| header missing `service_code`  | error, header-only result                 |
| missing body spec              | warning, header parsed, body as raw tail  |
| message truncated mid-field    | error, return fields parsed so far        |
| message longer than spec       | warning, expose `unparsed_tail`           |
| invalid spec syntax            | `ValueError` with file:line context       |

---

## Tests

```bash
pytest -q
```

CI runs Ubuntu / Windows / macOS on Python 3.10–3.12. See
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## Roadmap

```
v0.1   sequential parser, dispatcher, CLI, Neovim integration    (this release)
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
