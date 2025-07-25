"""Простейшая реализация динамического тела."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pyrr import Vector3

from .collisions import Collider


@dataclass
class RigidBody:
    """Динамическое тело с интегратором Эйлера."""

    mass: float = 1.0
    velocity: Vector3 = field(default_factory=lambda: Vector3([0.0, 0.0, 0.0]))
    collider: Optional[Collider] = field(default=None)
    entity: Optional[object] = field(default=None, repr=False)

    _force: Vector3 = field(default_factory=lambda: Vector3([0.0, 0.0, 0.0]), init=False, repr=False)

    def add_force(self, force: Vector3) -> None:
        """Прикладывает силу к телу."""
        self._force += force

    def integrate(self, dt: float) -> None:
        """Обновляет скорость и позицию с учётом накопленных сил."""
        if self.entity is None:
            return
        acceleration = self._force / self.mass
        self.velocity += acceleration * dt
        self.entity.position = Vector3(self.entity.position) + self.velocity * dt
        self._force = Vector3([0.0, 0.0, 0.0])
        if self.collider:
            self.collider.entity = self.entity
