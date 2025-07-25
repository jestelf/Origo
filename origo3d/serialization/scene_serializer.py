"""Сохранение и загрузка сцен."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from ..scene import Scene
from .format_json import read_json, write_json

LOCAL_SAVE_DIR = Path("saves")
CLOUD_SAVE_DIR = Path("cloud/saves")


def save_scene(scene: Scene, path: Optional[Path] = None, cloud: bool = False) -> Path:
    """Сохранить сцену на диск или в облако."""
    if path is None:
        directory = CLOUD_SAVE_DIR if cloud else LOCAL_SAVE_DIR
        path = directory / f"{scene.name}.json"
    write_json(path, scene.to_dict())
    return path


def load_scene(name: str, path: Optional[Path] = None, cloud: bool = False, entity_ids: Optional[Iterable[int]] = None) -> Scene:
    """Загрузить сцену. Можно указать список ``entity_ids`` для выборочной загрузки."""
    if path is None:
        directory = CLOUD_SAVE_DIR if cloud else LOCAL_SAVE_DIR
        path = directory / f"{name}.json"
    data = read_json(path)
    scene = Scene.from_dict(data)
    if entity_ids is not None:
        scene.entities = [e for e in scene.entities if e.id in set(entity_ids)]
    return scene
