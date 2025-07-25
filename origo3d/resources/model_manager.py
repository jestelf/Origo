"""Загрузка и кеширование OBJ-моделей."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

from .manifest import AssetManifest


class ModelManager:
    """Загружает геометрию моделей и кэширует их."""

    def __init__(self, manifest: AssetManifest | None = None) -> None:
        self.manifest = manifest or AssetManifest()
        self._models: Dict[str, np.ndarray] = {}

    def import_model(self, path: Path) -> str:
        """Добавить модель в манифест и вернуть её GUID."""
        return self.manifest.import_resource(path)

    def get(self, guid: str) -> np.ndarray:
        if guid in self._models:
            return self._models[guid]
        data = self.manifest.load(guid)
        if data is None:
            raise FileNotFoundError(f"Model with GUID {guid} not found")
        vertices: list[tuple[float, float, float]] = []
        indices: list[int] = []
        for line in data.decode("utf-8").splitlines():
            if line.startswith("v "):
                _, x, y, z = line.split()[:4]
                vertices.append((float(x), float(y), float(z)))
            elif line.startswith("f "):
                parts = line.split()[1:]
                indices.extend(int(p.split("/")[0]) - 1 for p in parts)
        result: list[float] = []
        for idx in indices:
            result.extend(vertices[idx])
        arr = np.array(result, dtype="f4")
        self._models[guid] = arr
        return arr

    def load_obj(self, path: Path) -> np.ndarray:
        """Импортировать OBJ и вернуть геометрию."""
        guid = self.import_model(path)
        return self.get(guid)

    def search_models(self, keyword: str):
        """Найти модели по ключевому слову."""
        return self.manifest.search(keyword)
