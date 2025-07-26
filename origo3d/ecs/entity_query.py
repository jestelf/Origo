from __future__ import annotations

from typing import Iterable, List, Type, Any

from .entity_manager import EntityManager


class EntityQuery:
    """Запрос сущностей по набору компонентов."""

    def __init__(self, manager: EntityManager, *component_types: Type[Any]) -> None:
        self.manager = manager
        self.component_types = component_types

    def ids(self) -> List[int]:
        """Список id подходящих сущностей."""
        return self.manager.get_entities_with(*self.component_types)

    def entities(self) -> Iterable[Any]:
        """Итератор по сущностям, удовлетворяющим запросу."""
        for eid in self.ids():
            yield self.manager.entities[eid]

    def __iter__(self):
        return self.entities()

