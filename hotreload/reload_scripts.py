"""Подсистема для горячего обновления скриптов поведения."""

from __future__ import annotations

from typing import Iterable

from .hotreloader import HotReloader


def setup_script_reloading(reloader: HotReloader, modules: Iterable[str]) -> None:
    """Отслеживать изменения указанных модулей."""
    for mod in modules:
        reloader.watch_module(mod)
