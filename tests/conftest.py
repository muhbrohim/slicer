"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def tmp_specs(tmp_path: Path) -> Path:
    """An empty specs root with `body/` already created."""
    (tmp_path / "body").mkdir()
    return tmp_path


def write_spec(root: Path, name: str, body: str) -> Path:
    """Write `body` to `root/{name}` and return the path."""
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path
