"""(Де)сериализация сущностей."""

from __future__ import annotations

from typing import Any, Dict

from origo3d.scene.entity import Entity


def entity_to_dict(entity: Entity) -> Dict[str, Any]:
    """Преобразовать :class:`Entity` в словарь."""
    return entity.to_dict()


def entity_from_dict(data: Dict[str, Any]) -> Entity:
    """Создать :class:`Entity` из словаря."""
    return Entity.from_dict(data)
