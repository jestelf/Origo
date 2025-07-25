"""Origo CLI и система загрузки плагинов."""

from __future__ import annotations

import importlib
import os
import pkgutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Iterable, List, Any

PLUGIN_ENV = "ORIGO_CLI_PLUGIN_PATHS"
BUILTIN_DIR = Path(__file__).resolve().parent / "plugins"


def _iter_modules(paths: Iterable[Path]) -> Iterable[ModuleType]:
    for path in paths:
        if not path.is_dir():
            continue
        sys.path.insert(0, str(path))
        for _, name, _ in pkgutil.iter_modules([str(path)]):
            # Если путь внутри пакета origo_cli.plugins, импортируем с префиксом
            if path == BUILTIN_DIR:
                module = importlib.import_module(f"origo_cli.plugins.{name}")
            else:
                module = importlib.import_module(name)
            yield module


def load_plugins(
    cli: Any | None = None, paths: Iterable[str] | None = None
) -> List[ModuleType]:
    """Загружает все плагины из стандартных и пользовательских каталогов."""
    search_paths = []
    if paths is None:
        env = os.environ.get(PLUGIN_ENV, "")
        search_paths.append(BUILTIN_DIR)
        if env:
            search_paths.extend(Path(p) for p in env.split(os.pathsep) if p)
    else:
        search_paths.extend(Path(p) for p in paths)

    modules: List[ModuleType] = []
    for module in _iter_modules(search_paths):
        if hasattr(module, "register"):
            module.register(cli)
        modules.append(module)
    return modules
