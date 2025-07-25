"""Пакет для (де)сериализации сцен и компонентов."""

from .component_serializer import entity_from_dict, entity_to_dict
from .scene_serializer import load_scene, save_scene

__all__ = [
    "entity_from_dict",
    "entity_to_dict",
    "load_scene",
    "save_scene",
]
