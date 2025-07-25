"""Сцена, содержащая сущности и физическую систему."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from origo3d.physics.physics_system import PhysicsSystem
from .entity import Entity


@dataclass
class Scene:
    """Простая сцена с коллекцией сущностей."""

    entities: List[Entity] = field(default_factory=list)
    physics: PhysicsSystem = field(default_factory=PhysicsSystem)

    def add_entity(self, entity: Entity) -> None:
        """Добавить сущность и зарегистрировать её в физике."""
        self.entities.append(entity)
        self.physics.register_entity(entity)

    def update(self, dt: float) -> None:
        """Обновить физику сцены."""
        self.physics.update(dt)
