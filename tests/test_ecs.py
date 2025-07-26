from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origo3d.ecs.entity_manager import EntityManager
from origo3d.ecs.entity_query import EntityQuery
from origo3d.scene import Entity, Scene


class CompA:
    pass


class CompB:
    pass


def test_entity_manager_components_query() -> None:
    em = EntityManager()
    e1 = em.create_entity("e1")
    e2 = em.create_entity("e2")

    em.add_component(e1.id, CompA())
    em.add_component(e1.id, CompB())
    em.add_component(e2.id, CompA())

    q_a = EntityQuery(em, CompA)
    assert set(q_a.ids()) == {e1.id, e2.id}

    q_ab = EntityQuery(em, CompA, CompB)
    assert q_ab.ids() == [e1.id]

    em.remove_component(e1.id, CompB)
    assert q_ab.ids() == []


def test_scene_uses_entity_manager() -> None:
    scene = Scene()
    ent = Entity(10, "hero")
    scene.add_entity(ent)
    assert ent in scene.entities
    assert ent.id in scene.entity_manager.entities

    scene.remove_entity(ent)
    assert ent.id not in scene.entity_manager.entities
    assert ent not in scene.entities
