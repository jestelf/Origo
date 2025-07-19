"""Minimal application wrapper for opening a window."""

from __future__ import annotations

from typing import Dict

import logging
import time
import pyglet

from origo3d.rendering.renderer import Renderer


class Application:
    """Application creates a pyglet window based on configuration."""

    def __init__(self, graphics_cfg: Dict | None = None):
        self.settings = graphics_cfg or {}
        self.window: pyglet.window.Window | None = None
        self.renderer: Renderer | None = None
        self.running = False
        self.logger = logging.getLogger(__name__)

    def _create_window(self) -> None:
        width, height = self.settings.get("resolution", [800, 600])
        vsync = self.settings.get("vsync", True)
        title = self.settings.get("title", "Origo3D")
        self.logger.info("Creating window %sx%s", width, height)
        self.window = pyglet.window.Window(
            width=width,
            height=height,
            vsync=bool(vsync),
            caption=title,
        )

        self.renderer = Renderer()

        @self.window.event  # type: ignore
        def on_draw():
            if self.renderer:
                self.renderer.render_frame()

        @self.window.event  # type: ignore
        def on_close():
            self.logger.info("Window closed")
            self.running = False

    def run(self) -> None:
        if self.window is None:
            self._create_window()
        fps = float(self.settings.get("target_fps", 60))
        frame_time = 1.0 / fps
        self.logger.info("Starting main loop at %s FPS", fps)
        self.running = True
        last = time.perf_counter()
        while self.running:
            self.window.dispatch_events()
            now = time.perf_counter()
            dt = now - last
            last = now
            self.update(dt)
            if self.renderer:
                self.renderer.render_frame()
            self.window.flip()
            sleep = frame_time - (time.perf_counter() - now)
            if sleep > 0:
                time.sleep(sleep)
        self.logger.info("Main loop terminated")

    def update(self, dt: float) -> None:
        """Update application logic."""
        # Placeholder for future logic
        pass

