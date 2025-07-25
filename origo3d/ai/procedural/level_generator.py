"""Генератор простых геометрических уровней."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from runtime import env_settings


@dataclass
class LevelConfig:
    width: int = 20
    height: int = 15
    num_obstacles: int = 5
    obstacle_size: tuple[int, int] = (3, 3)
    seed: Optional[int] = None


def generate_level(config: LevelConfig | None = None) -> np.ndarray:
    """Создать двумерную сетку уровня, где 0 - пустота, 1 - препятствие."""
    if config is None:
        settings = env_settings.get("procedural", {}).get("level", {})
        if "obstacle_size" in settings and isinstance(settings["obstacle_size"], list):
            settings["obstacle_size"] = tuple(settings["obstacle_size"])
        config = LevelConfig(**settings)

    rng = np.random.default_rng(config.seed)
    grid = np.zeros((config.height, config.width), dtype=np.int8)

    # границы уровня
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1

    for _ in range(config.num_obstacles):
        w = rng.integers(1, config.obstacle_size[0] + 1)
        h = rng.integers(1, config.obstacle_size[1] + 1)
        x = rng.integers(1, config.width - w - 1)
        y = rng.integers(1, config.height - h - 1)
        grid[y : y + h, x : x + w] = 1

    return grid
