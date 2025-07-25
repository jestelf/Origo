"""Отслеживание изменений шейдеров."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .hotreloader import HotReloader


def watch_shader(reloader: HotReloader, shader_file: str | Path, on_reload: Callable[[Path], None]) -> None:
    """Следить за изменением GLSL-файла и вызывать обработчик."""
    reloader.watch_resource(shader_file, on_reload)
