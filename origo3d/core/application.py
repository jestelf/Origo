"""Minimal application wrapper for opening a window."""

from __future__ import annotations

from typing import Dict, List

import logging
import time

from devtools.performance_monitor import PerformanceMonitor
import pyglet
from pyglet.window import NoSuchDisplayException
from pyglet import text

from origo3d.rendering.renderer import Renderer

class Application:
    """Application creates a pyglet window based on configuration."""

    def __init__(self, graphics_cfg: Dict | None = None, enable_monitor: bool = False):
        self.settings = graphics_cfg or {}
        self.window: pyglet.window.Window | None = None
        self.renderer: Renderer | None = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        self.monitor: PerformanceMonitor | None = PerformanceMonitor() if enable_monitor else None
        self.overlay_label: text.Label | None = None

    def _create_window(self) -> None:
        width, height = self.settings.get("resolution", [800, 600])
        vsync = self.settings.get("vsync", True)
        title = self.settings.get("title", "Origo3D")
        self.logger.info("Creating window %sx%s", width, height)
        try:
            self.window = pyglet.window.Window(
                width=width,
                height=height,
                vsync=bool(vsync),
                caption=title,
            )
        except NoSuchDisplayException:  # pragma: no cover - depends on env
            self.logger.warning("No display available, enabling headless mode")
            pyglet.options["headless"] = True
            self.window = pyglet.window.Window(
                width=width,
                height=height,
                vsync=bool(vsync),
                caption=title,
            )

        api = self.settings.get("api", "opengl")
        self.renderer = Renderer(width=width, height=height, api=api)

        if self.monitor:
            self.overlay_label = text.Label(
                "",
                x=10,
                y=height - 10,
                anchor_x="left",
                anchor_y="top",
                color=(255, 255, 255, 255),
            )

        @self.window.event  # type: ignore
        def on_draw():
            if self.renderer:
                self.renderer.render_frame()
            if self.monitor and self.overlay_label:
                self.overlay_label.draw()

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
            if self.monitor:
                self.monitor.start_frame()

            self.window.dispatch_events()
            now = time.perf_counter()
            dt = now - last
            last = now

            if self.monitor:
                self.monitor.start_subsystem("update")
            self.update(dt)
            if self.monitor:
                self.monitor.end_subsystem("update")

            if self.renderer:
                if self.monitor:
                    self.monitor.start_subsystem("render")
                self.renderer.render_frame()
                if self.monitor:
                    self.monitor.end_subsystem("render")

            self.window.flip()

            if self.monitor:
                self.monitor.end_frame()
                if self.overlay_label:
                    self.overlay_label.text = self.monitor.report()

            sleep = frame_time - (time.perf_counter() - now)
            if sleep > 0:
                time.sleep(sleep)
        self.logger.info("Main loop terminated")

    def update(self, dt: float) -> None:
        """Update application logic."""
        # Placeholder for future logic
        pass

