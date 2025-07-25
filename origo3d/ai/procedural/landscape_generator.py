"""Генерация процедурного ландшафта."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from runtime import env_settings


@dataclass
class TerrainConfig:
    width: int = 64
    height: int = 64
    octaves: int = 4
    persistence: float = 0.5
    lacunarity: float = 2.0
    seed: Optional[int] = None


def _fractal_noise(cfg: TerrainConfig) -> np.ndarray:
    rng = np.random.default_rng(cfg.seed)
    noise = np.zeros((cfg.height, cfg.width), dtype=np.float32)
    frequency = 1.0
    amplitude = 1.0
    for _ in range(cfg.octaves):
        noise += amplitude * rng.random((cfg.height, cfg.width))
        frequency *= cfg.lacunarity
        amplitude *= cfg.persistence
    noise -= noise.min()
    if noise.max() > 0:
        noise /= noise.max()
    return noise


def generate_terrain(config: TerrainConfig | None = None) -> np.ndarray:
    """Сгенерировать высотную карту ландшафта."""
    if config is None:
        settings = env_settings.get("procedural", {}).get("terrain", {})
        config = TerrainConfig(**settings)
    return _fractal_noise(config)
