"""Горячая перезагрузка данных сцены."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .hotreloader import HotReloader


def watch_scene(reloader: HotReloader, scene_file: str | Path, on_reload: Callable[[Path], None]) -> None:
    """Отслеживать изменения JSON-файла сцены и вызывать обработчик."""
    reloader.watch_resource(scene_file, on_reload)
