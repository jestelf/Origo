"""Простейшая сущность сцены."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from pyrr import Vector3


@dataclass
class Entity:
    """Объект сцены с позицией и компонентами."""

    name: str = ""
    position: Vector3 = field(default_factory=lambda: Vector3([0.0, 0.0, 0.0]))
    components: List[object] = field(default_factory=list)

    def add_component(self, component: object) -> object:
        """Добавить компонент к сущности."""
        self.components.append(component)
        if hasattr(component, "entity"):
            component.entity = self
        return component
