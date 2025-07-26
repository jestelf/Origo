from __future__ import annotations

from typing import Any, Iterable, Type

from .entity_manager import EntityManager
from .entity_query import EntityQuery


class System:
    """Базовый класс для систем ECS."""

    def __init__(self, manager: EntityManager, *component_types: Type[Any]) -> None:
        self.manager = manager
        self.component_types = component_types
        self.query = EntityQuery(manager, *component_types)

    def update(self, dt: float) -> None:  # pragma: no cover - для наследников
        """Обновить систему. Должен быть переопределён в наследниках."""
        raise NotImplementedError

    def entities(self) -> Iterable[Any]:
        """Итерация по подходящим сущностям."""
        return self.query.entities()

