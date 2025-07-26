"""Запуск сохранённой сцены с использованием ECS."""

from __future__ import annotations

from origo3d.serialization.scene_serializer import load_scene
from origo3d.physics import RigidBody


def run(scene_name: str) -> None:
    """Загрузить сцену, добавить тестовую сущность и запустить обновление."""
    scene = load_scene(scene_name)
    print(f"Running scene: {scene.name}")

    # пример добавления сущности через ECS
    ent = scene.create_entity("runner_entity")
    scene.entity_manager.add_component(ent.id, RigidBody())

    # небольшой цикл обновления
    for _ in range(5):
        scene.update(0.016)
