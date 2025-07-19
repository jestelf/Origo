"""Minimal application wrapper for opening a window."""

from __future__ import annotations

from typing import Dict, List

import pyglet


class Application:
    """Application creates a pyglet window based on configuration."""

    def __init__(self, graphics_cfg: Dict | None = None):
        self.settings = graphics_cfg or {}
        self.window: pyglet.window.Window | None = None

    def _create_window(self) -> None:
        width, height = self.settings.get("resolution", [800, 600])
        vsync = self.settings.get("vsync", True)
        self.window = pyglet.window.Window(
            width=width,
            height=height,
            vsync=bool(vsync),
            caption="Origo3D",
        )

        @self.window.event
        def on_draw():  # type: ignore
            self.window.clear()

    def run(self) -> None:
        if self.window is None:
            self._create_window()
        pyglet.app.run()

