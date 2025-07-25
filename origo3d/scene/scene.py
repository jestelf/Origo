from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import threading
import time

from .entity import Entity


@dataclass
class Scene:
    """Содержит набор сущностей и поддерживает автосохранение."""

    name: str
    entities: List[Entity] = field(default_factory=list)
    _autosave_thread: threading.Thread | None = field(default=None, init=False, repr=False)
    _stop_autosave: bool = field(default=False, init=False, repr=False)

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "entities": [e.to_dict() for e in self.entities],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Scene":
        scene = cls(name=str(data.get("name", "scene")))
        scene.entities = [Entity.from_dict(d) for d in data.get("entities", [])]
        return scene

    def autosave(self, interval: float = 60.0, cloud: bool = False, path: Optional[Path] = None) -> None:
        """Запустить периодическое сохранение сцены."""
        if self._autosave_thread:
            return

        from origo3d.serialization.scene_serializer import save_scene  # локальный импорт во избежание циклов

        if path is None:
            filename = f"{self.name}_autosave.json"
            path = Path(filename)

        def worker() -> None:
            while not self._stop_autosave:
                save_scene(self, path=path, cloud=cloud)
                time.sleep(interval)

        self._stop_autosave = False
        self._autosave_thread = threading.Thread(target=worker, daemon=True)
        self._autosave_thread.start()

    def stop_autosave(self) -> None:
        if not self._autosave_thread:
            return
        self._stop_autosave = True
        self._autosave_thread.join()
        self._autosave_thread = None
