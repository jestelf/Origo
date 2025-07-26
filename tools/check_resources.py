#!/usr/bin/env python3
"""Поиск проблем с ресурсами и сценами."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ASSETS_DIR = Path("assets")
SCENES_DIR = Path("scenes")
VERSION_FILE = Path("asset_versioning.json")
MANIFEST_FILE = ASSETS_DIR / "manifest.json"


def find_missing_assets() -> list[str]:
    """Возвращает список отсутствующих файлов из манифестов."""
    missing: list[str] = []
    if VERSION_FILE.exists():
        data = json.loads(VERSION_FILE.read_text())
        for path_str in data:
            norm = Path(path_str.replace("\\", "/"))
            if not norm.exists():
                missing.append(path_str)
    if MANIFEST_FILE.exists():
        data = json.loads(MANIFEST_FILE.read_text())
        for path_str in data.values():
            norm = Path(path_str.replace("\\", "/"))
            if not norm.exists():
                missing.append(path_str)
    return missing


def find_duplicate_names(root: Path) -> dict[str, list[str]]:
    """Ищет файлы с одинаковыми именами внутри каталога."""
    seen: dict[str, str] = {}
    dups: dict[str, list[str]] = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            if path.name in seen:
                if not dups[path.name]:
                    dups[path.name].append(seen[path.name])
                dups[path.name].append(str(path))
            else:
                seen[path.name] = str(path)
    return dups


def main() -> int:
    missing = find_missing_assets()
    dup_assets = find_duplicate_names(ASSETS_DIR)
    dup_scenes = find_duplicate_names(SCENES_DIR)

    if missing:
        print("Отсутствующие файлы:")
        for m in missing:
            print(f"  {m}")
    if dup_assets:
        print("Дубли имён в assets/:")
        for name, paths in dup_assets.items():
            joined = ", ".join(paths)
            print(f"  {name}: {joined}")
    if dup_scenes:
        print("Дубли имён в scenes/:")
        for name, paths in dup_scenes.items():
            joined = ", ".join(paths)
            print(f"  {name}: {joined}")

    if not (missing or dup_assets or dup_scenes):
        print("Проблем не найдено.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
