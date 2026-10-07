"""Configuration and state paths for KundALLY Panel."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any


APP_ID = "kundally-panel"

DEFAULT_CONFIG: dict[str, Any] = {
    "title": "KundALLY",
    "language": "tr",
    "countdown_target": "2027-08-15T00:00:00",
    "show_countdown": True,
    "show_public_ip": True,
    "show_local_ip": True,
    "show_location": True,
    "manual_city": "",
    "always_on_top": True,
    "accent_color": "#00e5ff",
    "panel_width": 190,
}


def xdg_path(variable: str, fallback: str) -> Path:
    return Path(os.environ.get(variable, str(Path.home() / fallback))).expanduser()


CONFIG_DIR = xdg_path("XDG_CONFIG_HOME", ".config") / APP_ID
STATE_DIR = xdg_path("XDG_STATE_HOME", ".local/state") / APP_ID
CONFIG_FILE = CONFIG_DIR / "config.json"
POSITION_FILE = STATE_DIR / "position.json"
PID_FILE = STATE_DIR / "panel.pid"
LOCK_FILE = STATE_DIR / "panel.lock"


def normalize_config(candidate: dict[str, Any]) -> dict[str, Any]:
    """Merge known, correctly typed values into the defaults."""
    result = deepcopy(DEFAULT_CONFIG)
    for key, default in DEFAULT_CONFIG.items():
        value = candidate.get(key)
        if key == "language":
            if value in ("tr", "en"):
                result[key] = value
            continue
        if isinstance(default, bool):
            if isinstance(value, bool):
                result[key] = value
        elif isinstance(default, int):
            if isinstance(value, int) and not isinstance(value, bool):
                result[key] = max(160, min(420, value)) if key == "panel_width" else value
        elif isinstance(default, str):
            if isinstance(value, str) and value.strip():
                result[key] = value.strip()
    return result


def load_config(path: Path = CONFIG_FILE) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return normalize_config(raw if isinstance(raw, dict) else {})
    except (OSError, json.JSONDecodeError):
        return deepcopy(DEFAULT_CONFIG)


def save_config(config: dict[str, Any], path: Path = CONFIG_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(normalize_config(config), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def load_position(path: Path = POSITION_FILE) -> tuple[int, int] | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return int(raw["x"]), int(raw["y"])
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def save_position(x: int, y: int, path: Path = POSITION_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"x": x, "y": y}) + "\n", encoding="utf-8")
