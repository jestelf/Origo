"""Entry point for launching the engine."""

import logging

from origo3d.core.application import Application
from runtime import env_settings

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
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