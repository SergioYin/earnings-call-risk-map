"""JSON input and output helpers."""

from __future__ import annotations

import json
import re
from datetime import date
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from .models import REQUIRED_TOP_LEVEL

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def read_json(path: str | Path) -> dict[str, Any]:
    """Read a JSON object from disk and validate its top-level shape."""

    source = Path(path)
    try:
        with source.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except JSONDecodeError as exc:
        raise ValueError(f"{source} is not valid JSON at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{source} must contain a JSON object")
    validate_input(data, str(source))
    return data


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    _ensure_file_target(target)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    _ensure_file_target(target)
    target.write_text(text, encoding="utf-8")


def _ensure_file_target(target: Path) -> None:
    parent = target.parent
    if parent.exists() and not parent.is_dir():
        raise ValueError(f"cannot write {target}: parent path {parent} is not a directory")
    if target.exists() and target.is_dir():
        raise ValueError(f"cannot write {target}: output path is a directory")
    parent.mkdir(parents=True, exist_ok=True)


def validate_input(data: dict[str, Any], label: str = "input") -> None:
    missing = [field for field in REQUIRED_TOP_LEVEL if not data.get(field)]
    if missing:
        raise ValueError(f"{label} is missing required field(s): {', '.join(missing)}")
    for field in ("company", "ticker"):
        if not isinstance(data[field], str):
            raise ValueError(f"{label}.{field} must be a non-empty string")
    for field in ("as_of", "data_cutoff"):
        _validate_date(data[field], f"{label}.{field}")
    for collection in ("notes", "catalysts", "kpis"):
        if collection in data and not isinstance(data[collection], list):
            raise ValueError(f"{label}.{collection} must be a list when provided")
        for index, item in enumerate(data.get(collection, [])):
            if not isinstance(item, dict):
                raise ValueError(f"{label}.{collection}[{index}] must be a JSON object")
            if item.get("date"):
                _validate_date(item["date"], f"{label}.{collection}[{index}].date")


def _validate_date(value: Any, field: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string in YYYY-MM-DD format")
    if not DATE_RE.match(value):
        raise ValueError(f"{field} must use YYYY-MM-DD format, got {value!r}")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid calendar date, got {value!r}") from exc
