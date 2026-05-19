# Changelog

All notable changes to slicer are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `@repeat <group> <count>` ... `@end` directive in the spec language for
  fixed-count repeating record blocks (e.g. 20-element customer arrays).
- Parser emits each iteration's fields as `group[NN].field` (1-indexed,
  two-digit).
- JSON output collapses repeat groups into a real nested array under the
  group name.
- `ScalarField` / `RepeatGroup` types exposed from `slicer` for programmatic
  consumers.
- Real production sample: `sample_messages/us1003_real.txt` + matching
  `specs/header.spec` (220-byte DSVI-HDR-INFO) + `specs/body/#US1003.spec`.

### Removed
- Toy demo specs `CA1017.spec`, `CA2020.spec`, and `ca1017_demo.txt`.

## [0.1.0] - 2026-05-19

### Added
- Plaintext `.spec` format: `field_name length` per line, `#` comments.
- `slicer.spec_loader` — load and validate spec files.
- `slicer.parser.sequential_parse` — pure offset slicer.
- `slicer.dispatcher.parse_message` — header → service_code → body orchestration.
- `slicer.formatter` — rich table, JSON, raw key=value, offset view.
- `slicer.detector` — fallback service_code search.
- `slice` CLI: positional / stdin / interactive input, `--json --raw --offsets`.
- `spec` CLI: `list`, `show`, `create`.
- Neovim plugin (`nvim/slicer.lua`) with `<leader>sp/ss/so` keymaps.
- Sample header + body specs (`CA1017`, `CA2020`) and a sample message.
- pytest suite for parser, spec_loader, dispatcher.
- GitHub Actions CI matrix (Ubuntu / Windows / macOS × Python 3.10–3.12).
- MIT license.
