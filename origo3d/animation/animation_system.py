from __future__ import annotations

"""Система обновления компонентов :class:`Animator`."""

from ..ecs.entity_manager import EntityManager
from ..ecs.system import System

from .animator import Animator


class AnimationSystem(System):
    """Простейшая система анимации."""

    def __init__(self, manager: EntityManager) -> None:
        super().__init__(manager, Animator)

    def update(self, dt: float) -> None:
        for entity in self.entities():
            animator = self.manager.get_component(entity.id, Animator)
            if animator:
                animator.update(dt)
