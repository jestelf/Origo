"""Entry point with simple launcher for the engine and tools."""

from __future__ import annotations

import logging

import pyglet
from origo3d.core.application import Application
from runtime import env_settings
from editor.scene_editor import SceneEditor


class Launcher(pyglet.window.Window):
    """Minimal graphical launcher."""

    def __init__(self) -> None:
        super().__init__(400, 300, "Origo3D Launcher")
        self.selection: str | None = None
        self.label = pyglet.text.Label(
            "1 – Запустить движок\n"
            "2 – Редактор сцен\n"
            "3 – Полный редактор\n"
            "Esc – выход",
            anchor_x="center",
            anchor_y="center",
            x=self.width // 2,
            y=self.height // 2,
            multiline=True,
            width=self.width - 20,
        )

    def on_draw(self) -> None:  # pragma: no cover - GUI
        self.clear()
        self.label.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:  # pragma: no cover - GUI
        if symbol == pyglet.window.key._1:
            self.selection = "engine"
            self.close()
        elif symbol == pyglet.window.key._2:
            self.selection = "editor"
            self.close()
        elif symbol == pyglet.window.key._3:
            self.selection = "full_editor"
            self.close()
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()


def run_engine() -> None:
    """Launch the main application loop."""
    logging.info("Loading configuration")
    config = env_settings.load()
    graphics_cfg = config.get("graphics", {})
    app = Application(graphics_cfg, enable_monitor=True)
    logging.info("Starting application")
    try:
        app.run()
    except Exception as exc:  # pragma: no cover - runtime failure
        logging.error("Application crashed: %s", exc)
        raise


def run_editor() -> None:
    """Open the simple scene editor."""
    editor = SceneEditor()
    pyglet.app.run()


def run_full_editor() -> None:
    """Launch the multi-window editor."""
    from editor.full_editor import FullEditor
    FullEditor()
    pyglet.app.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    launcher = Launcher()
    pyglet.app.run()

    if launcher.selection == "engine":
        run_engine()
    elif launcher.selection == "editor":
        run_editor()
    elif launcher.selection == "full_editor":
        run_full_editor()
