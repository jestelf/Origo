# Basic configuration loader for engine settings

"""Load YAML configuration files for the engine.

This module reads :code:`config.yaml` in the repository root and all
``.yaml`` files under the ``configs/`` directory. Settings are returned as a
nested dictionary accessible via :func:`load` and :func:`get`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


_BASE_CONFIG = Path("config.yaml")
_CONFIG_DIR = Path("configs")

_settings: Dict[str, Any] = {}


def _load_yaml(file: Path) -> Dict[str, Any]:
    """Return contents of a YAML file or an empty dict if it does not exist."""
    if not file.exists():
        return {}
    with file.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load() -> Dict[str, Any]:
    """Load configuration files and return the resulting settings."""
    global _settings
    data: Dict[str, Any] = {}

    # Load base config
    data.update(_load_yaml(_BASE_CONFIG))

    # Load individual configs from configs directory
    if _CONFIG_DIR.exists():
        for path in _CONFIG_DIR.glob("*.yaml"):
            data[path.stem] = _load_yaml(path)

    _settings = data
    return _settings


def get(section: str | None = None, default: Any | None = None) -> Any:
    """Return a section from the loaded configuration."""
    if not _settings:
        load()
    if section is None:
        return _settings
    return _settings.get(section, default)

