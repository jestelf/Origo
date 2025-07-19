"""Entry point for launching the engine."""

from origo3d.core.application import Application
from runtime import env_settings

if __name__ == "__main__":
    config = env_settings.load()
    graphics_cfg = config.get("graphics", {})
    app = Application(graphics_cfg)
    app.run()
