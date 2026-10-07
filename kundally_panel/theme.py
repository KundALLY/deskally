"""Command-line color presets for KundALLY Panel."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .config import CONFIG_FILE, load_config, save_config


PALETTE = {
    "turkuaz": "#00e5ff",
    "mavi": "#3b82f6",
    "kirmizi": "#ff3b5c",
    "yesil": "#22c55e",
    "mor": "#a855f7",
    "altin": "#f5b942",
}


def resolve_color(value: str) -> str:
    normalized = value.strip().lower().replace("ı", "i").replace("ş", "s")
    color = PALETTE.get(normalized, value.strip())
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        choices = ", ".join(PALETTE)
        raise ValueError(f"Bilinmeyen renk: {value}. Seçenekler: {choices} veya #RRGGBB")
    return color.lower()


def set_accent(value: str, path: Path = CONFIG_FILE) -> str:
    """Change only the accent color and preserve every other setting."""
    color = resolve_color(value)
    config = load_config(path)
    config["accent_color"] = color
    save_config(config, path)
    return color


def main(arguments: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if arguments is None else arguments)
    if len(arguments) != 1:
        print("Kullanım: kundally-panel color RENK", file=sys.stderr)
        print("Renkler: " + ", ".join(PALETTE), file=sys.stderr)
        return 2
    try:
        color = set_accent(arguments[0])
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    print(f"KundALLY Panel rengi değiştirildi: {color}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
