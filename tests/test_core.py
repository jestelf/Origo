"""Базовые юнит-тесты инициализации движка."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origo3d.core.application import Application
from runtime import env_settings


def test_load_config():
    cfg = env_settings.load()
    assert isinstance(cfg, dict)
    assert "graphics" in cfg
    assert cfg["graphics"].get("api") == "opengl"


def test_application_init():
    app = Application({"resolution": [320, 240], "vsync": False, "api": "opengl"})
    assert app.settings["resolution"] == [320, 240]

