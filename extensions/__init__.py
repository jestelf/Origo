"""Загрузчик внешних расширений Origo."""

from __future__ import annotations

import importlib
import os
import pkgutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Iterable, List, Any

EXT_PATHS_ENV = "ORIGO_EXT_PATHS"
DEFAULT_DIR = Path(__file__).resolve().parent


def _iter_modules(paths: Iterable[Path]) -> Iterable[ModuleType]:
    for path in paths:
        if not path.is_dir():
            continue
        sys.path.insert(0, str(path))
        for _, name, _ in pkgutil.iter_modules([str(path)]):
            yield importlib.import_module(name)


def load_extensions(
    engine: Any | None = None, paths: Iterable[str] | None = None
) -> List[ModuleType]:
    """Загрузить все расширения из указанных директорий.

    * ``engine`` – объект движка, передаваемый расширениям.
    * ``paths`` – список каталогов с расширениями. По умолчанию берётся
      каталог ``extensions`` в корне проекта и пути из переменной
      окружения ``ORIGO_EXT_PATHS`` (через ``:``).
    """
    search_paths = []
    if paths is None:
        env = os.environ.get(EXT_PATHS_ENV, "")
        search_paths.append(DEFAULT_DIR)
        if env:
            search_paths.extend(Path(p) for p in env.split(os.pathsep) if p)
    else:
        search_paths.extend(Path(p) for p in paths)

    modules: List[ModuleType] = []
    for module in _iter_modules(search_paths):
        if hasattr(module, "init_extension"):
            module.init_extension(engine)
        modules.append(module)
    return modules
