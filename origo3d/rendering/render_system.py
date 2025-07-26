from __future__ import annotations

"""Простейшая система рендеринга через ECS."""

from dataclasses import dataclass

from ..ecs.entity_manager import EntityManager
from ..ecs.system import System

from .renderer import Renderer


@dataclass
class RenderComponent:
    """Компонент, помечающий сущность как отрисовываемую."""

    model_path: str = ""


class RenderingSystem(System):
    """Минимальная обвязка для вызова :class:`Renderer`."""

    def __init__(self, manager: EntityManager, renderer: Renderer | None = None) -> None:
        super().__init__(manager, RenderComponent)
        self.renderer = renderer or Renderer()

    def update(self, dt: float) -> None:  # pragma: no cover - зависит от среды
        if list(self.query.ids()):
            self.renderer.render_frame()
