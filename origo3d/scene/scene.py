from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import threading
import time

from pyrr import Vector3  # если понадобится для Entity
from origo3d.physics.physics_system import PhysicsSystem
from origo3d.ecs.entity_manager import EntityManager

from .entity import Entity


@dataclass
class Scene:
    """Сцена с набором сущностей и системами ECS."""
    name: str = "scene"
    physics: PhysicsSystem | None = field(default=None)
    entity_manager: EntityManager = field(default_factory=EntityManager)

    # для автосохранения (не сериализуются)
    _autosave_thread: threading.Thread | None = field(default=None, init=False, repr=False)
    _stop_autosave: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.physics is None:
            self.physics = PhysicsSystem(self.entity_manager)

    @property
    def entities(self) -> list[Entity]:
        """Текущие сущности в сцене."""
        return list(self.entity_manager.entities.values())

    def create_entity(self, name: str = "") -> Entity:
        """Создать новую сущность через ``EntityManager``."""
        entity = self.entity_manager.create_entity(name)
        return entity

    def add_entity(self, entity: Entity) -> None:
        """Зарегистрировать готовую сущность в менеджере."""
        self.entity_manager.add_entity(entity)

    def remove_entity(self, entity: Entity | int | str) -> None:
        """Удалить сущность из сцены и отписать её от физики."""
        if not isinstance(entity, Entity):
            ent = self.entity_manager.entities.get(int(entity))
            if ent is None:
                return
            entity = ent
        self.entity_manager.remove_entity(entity.id)

    def update(self, dt: float) -> None:
        """Обновить физику сцены за интервал dt (в секундах)."""
        if self.physics:
            self.physics.update(dt)

    def to_dict(self) -> dict:
        """
        Преобразовать сцену в словарь для сериализации.
        Позиция сущностей и компоненты сериализуются через их to_dict.
        Физика в словарь не включается.
        """
        return {
            "name": self.name,
            "entities": [e.to_dict() for e in self.entities],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Scene:
        """
        Восстановить сцену из словаря.
        Сущности создаются через Entity.from_dict,
        а затем регистрируются в физике.
        """
        scene = cls(name=str(data.get("name", "scene")))
        for ent_data in data.get("entities", []):
            ent = Entity.from_dict(ent_data)
            scene.add_entity(ent)
        return scene

    def autosave(self,
                 interval: float = 60.0,
                 cloud: bool = False,
                 path: Optional[Path] = None) -> None:
        """
        Запустить фоновое автосохранение сцены.
        
        :param interval: интервал между сохранениями в секундах
        :param cloud: если True — сохранять «в облако» (реализовано в save_scene)
        :param path: путь к файлу; по умолчанию "{name}_autosave.json"
        """
        if self._autosave_thread:
            return  # уже запущено

        if path is None:
            path = Path(f"{self.name}_autosave.json")

        self._stop_autosave = False

        def _worker() -> None:
            from origo3d.serialization.scene_serializer import save_scene
            while not self._stop_autosave:
                save_scene(self, path=path, cloud=cloud)
                time.sleep(interval)

        self._autosave_thread = threading.Thread(target=_worker, daemon=True)
        self._autosave_thread.start()

    def stop_autosave(self) -> None:
        """Остановить фоновое автосохранение, если оно запущено."""
        if not self._autosave_thread:
            return
        self._stop_autosave = True
        self._autosave_thread.join()
        self._autosave_thread = None
