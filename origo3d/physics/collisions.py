"""Базовые классы коллайдеров и простая проверка столкновений."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pyrr import Vector3


@dataclass
class Collider:
    """Базовый коллайдер, привязанный к сущности."""

    radius: float = 0.0
    entity: Optional[object] = field(default=None, repr=False)

    @property
    def position(self) -> Vector3:
        """Текущая позиция из сущности."""
        if self.entity is None:
            return Vector3([0.0, 0.0, 0.0])
        return Vector3(self.entity.position)

    def check_collision(self, other: "Collider") -> bool:
        """Виртуальный метод проверки столкновения."""
        raise NotImplementedError


@dataclass
class SphereCollider(Collider):
    """Сферический коллайдер."""

    radius: float = 1.0

    def check_collision(self, other: Collider) -> bool:  # pragma: no cover - логику сложно протестировать
        if not isinstance(other, SphereCollider):
            return False
        diff = self.position - other.position
        distance_sq = diff.length_squared
        return distance_sq <= (self.radius + other.radius) ** 2


@dataclass
class AABBCollider(Collider):
    """Простой осево-ориентированный bbox."""

    size: Vector3 = field(default_factory=lambda: Vector3([1.0, 1.0, 1.0]))

    def check_collision(self, other: Collider) -> bool:  # pragma: no cover - логику сложно протестировать
        if not isinstance(other, AABBCollider):
            return False
        a_pos = self.position
        b_pos = other.position
        for i in range(3):
            if abs(a_pos[i] - b_pos[i]) > (self.size[i] / 2 + other.size[i] / 2):
                return False
        return True
