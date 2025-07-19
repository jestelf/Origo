"""Загрузка простых OBJ-моделей."""

from __future__ import annotations

from pathlib import Path

import numpy as np


class ModelManager:
    """Загружает геометрию моделей."""

    def load_obj(self, path: Path) -> np.ndarray:
        """Считать OBJ-файл и вернуть массив вершин."""
        vertices: list[tuple[float, float, float]] = []
        indices: list[int] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("v "):
                    _, x, y, z = line.split()[:4]
                    vertices.append((float(x), float(y), float(z)))
                elif line.startswith("f "):
                    parts = line.split()[1:]
                    indices.extend(int(p.split("/")[0]) - 1 for p in parts)
        result: list[float] = []
        for idx in indices:
            result.extend(vertices[idx])
        return np.array(result, dtype="f4")
