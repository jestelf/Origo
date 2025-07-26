from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Set, Type, TypeVar


T = TypeVar("T")


class EntityManager:
    """Простейший менеджер сущностей и компонентов."""

    def __init__(self) -> None:
        self._next_id: int = 1
        self.entities: Dict[int, "Entity"] = {}
        # индекс компонентов: тип -> множество id сущностей
        self._component_index: Dict[Type[Any], Set[int]] = defaultdict(set)

    # ------------------------------------------------------------------
    # Работа с сущностями
    # ------------------------------------------------------------------
    def create_entity(self, name: str = "") -> "Entity":
        """Создать сущность с уникальным идентификатором."""
        entity_id = self._next_id
        self._next_id += 1
        from origo3d.scene.entity import Entity

        ent = Entity(entity_id, name)
        self.entities[entity_id] = ent
        return ent

    def add_entity(self, entity: "Entity") -> None:
        """Зарегистрировать уже созданную сущность."""
        if entity.id in self.entities:
            raise ValueError(f"Entity id {entity.id} already exists")
        self.entities[entity.id] = entity
        for comp in entity.components.values():
            self._index_component(entity.id, comp)

    def remove_entity(self, entity_id: int) -> None:
        """Удалить сущность и все её компоненты."""
        ent = self.entities.pop(entity_id, None)
        if not ent:
            return
        for comp in list(ent.components.values()):
            self.remove_component(entity_id, type(comp))

    # ------------------------------------------------------------------
    # Работа с компонентами
    # ------------------------------------------------------------------
    def add_component(self, entity_id: int, component: Any) -> Any:
        """Добавить компонент сущности и обновить индексы."""
        ent = self.entities.get(entity_id)
        if ent is None:
            raise KeyError(f"Entity id {entity_id} not found")
        ent.add_component(component)
        self._index_component(entity_id, component)
        return component

    def remove_component(self, entity_id: int, component_type: Type[Any]) -> None:
        ent = self.entities.get(entity_id)
        if ent is None:
            return
        comp = None
        for key, value in list(ent.components.items()):
            if isinstance(value, component_type):
                comp = ent.components.pop(key)
                break
        if comp is not None:
            self._component_index[component_type].discard(entity_id)

    def get_component(self, entity_id: int, component_type: Type[T]) -> T | None:
        ent = self.entities.get(entity_id)
        if not ent:
            return None
        for value in ent.components.values():
            if isinstance(value, component_type):
                return value
        return None

    def get_entities_with(self, *component_types: Type[Any]) -> List[int]:
        """Вернуть id сущностей, имеющих все указанные компоненты."""
        if not component_types:
            return list(self.entities.keys())
        sets = [self._component_index.get(t, set()) for t in component_types]
        if not sets:
            return []
        result = set(sets[0])
        for s in sets[1:]:
            result &= s
        return list(result)

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------
    def _index_component(self, entity_id: int, component: Any) -> None:
        self._component_index[type(component)].add(entity_id)

