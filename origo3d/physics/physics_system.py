"""Система, обновляющая все физические компоненты сцены."""

from __future__ import annotations

from typing import List

from ..ecs.entity_manager import EntityManager
from ..ecs.system import System
from .rigidbody import RigidBody


class PhysicsSystem(System):
    """Упрощённый физический менеджер, работающий через ECS."""

    def __init__(self, manager: EntityManager) -> None:
        super().__init__(manager, RigidBody)

    @property
    def rigidbodies(self) -> List[RigidBody]:
        """Текущий список физических тел."""
        ids = self.query.ids()
        result: List[RigidBody] = []
        for eid in ids:
            rb = self.manager.get_component(eid, RigidBody)
            if rb:
                result.append(rb)
        return result

    def update(self, dt: float) -> None:
        """Интегрировать все тела, найденные через ECS."""
        for rb in self.rigidbodies:
            rb.integrate(dt)
