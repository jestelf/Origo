from __future__ import annotations

import time
from pathlib import Path

from origo3d.scene import Entity, Scene
from origo3d.serialization.scene_serializer import save_scene, load_scene


def test_local_save_and_selective_load(tmp_path: Path) -> None:
    scene = Scene("sample")
    scene.add_entity(Entity(1, "player"))
    scene.add_entity(Entity(2, "enemy"))

    save_path = tmp_path / "sample.json"
    save_scene(scene, path=save_path)
    assert save_path.exists()

    loaded = load_scene("sample", path=save_path, entity_ids=[2])
    assert len(loaded.entities) == 1
    assert loaded.entities[0].id == 2


def test_cloud_save(tmp_path: Path) -> None:
    scene = Scene("cloudscene")
    cloud_path = tmp_path / "cloud" / "cloudscene.json"
    save_scene(scene, path=cloud_path, cloud=True)
    assert cloud_path.exists()


def test_autosave(tmp_path: Path) -> None:
    scene = Scene("auto")
    auto_path = tmp_path / "auto.json"
    scene.autosave(interval=0.5, path=auto_path)
    time.sleep(1.2)
    scene.stop_autosave()
    assert auto_path.exists()
