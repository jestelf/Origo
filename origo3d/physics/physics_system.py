"""Система, обновляющая все физические компоненты сцены."""

from __future__ import annotations

from typing import List

from .rigidbody import RigidBody


class PhysicsSystem:
    """Упрощённый физический менеджер."""

    def __init__(self) -> None:
        self.rigidbodies: List[RigidBody] = []

    def register_entity(self, entity: object) -> None:
        """Находит :class:`RigidBody` у сущности и регистрирует его."""
        for comp in getattr(entity, "components", []):
            if isinstance(comp, RigidBody):
                comp.entity = entity
                self.rigidbodies.append(comp)

    def update(self, dt: float) -> None:
        """Интегрировать все зарегистрированные тела."""
        for rb in self.rigidbodies:
            rb.integrate(dt)
