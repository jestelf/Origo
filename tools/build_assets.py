"""Скрипт оптимизации ассетов и отслеживания версий."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ASSET_DIR = Path("assets")
VERSION_FILE = Path("asset_versioning.json")


def compute_hash(path: Path) -> str:
    hasher = hashlib.md5()
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


def optimize_asset(path: Path) -> None:
    """Простая оптимизация: удаление пустых строк и пробелов."""
    if path.suffix.lower() == ".obj":
        lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
        path.write_text("\n".join(lines))


def build() -> None:
    versions: dict[str, str] = {}
    if VERSION_FILE.exists():
        versions.update(json.loads(VERSION_FILE.read_text()))
    for file in ASSET_DIR.rglob("*"):
        if file.is_file():
            optimize_asset(file)
            versions[str(file)] = compute_hash(file)
    VERSION_FILE.write_text(json.dumps(versions, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    build()
