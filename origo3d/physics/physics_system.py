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
        for comp in getattr(entity, "components", {}).values():
            if isinstance(comp, RigidBody):
                comp.entity = entity
                self.rigidbodies.append(comp)

    def unregister_entity(self, entity: object) -> None:
        """Удалить все связанные с сущностью тела из списка."""
        self.rigidbodies = [rb for rb in self.rigidbodies if rb.entity is not entity]

    def update(self, dt: float) -> None:
        """Интегрировать все зарегистрированные тела."""
        for rb in self.rigidbodies:
            rb.integrate(dt)
