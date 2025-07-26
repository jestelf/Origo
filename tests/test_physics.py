"""Тесты для базовой физики."""

from pathlib import Path
import sys

from pyrr import Vector3

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origo3d.scene import Scene
from origo3d.physics import RigidBody, SphereCollider


def test_rigidbody_motion():
    scene = Scene()
    ent = scene.create_entity("ball")
    rb = RigidBody(mass=1.0, collider=SphereCollider(radius=1.0))
    scene.entity_manager.add_component(ent.id, rb)

    rb.add_force(Vector3([0.0, 9.81, 0.0]))
    scene.update(1.0)

    assert ent.position.y > 0


def test_remove_entity_from_physics():
    scene = Scene()
    ent1 = scene.create_entity("e1")
    scene.entity_manager.add_component(ent1.id, RigidBody())
    ent2 = scene.create_entity("e2")
    scene.entity_manager.add_component(ent2.id, RigidBody())

    assert len(scene.physics.rigidbodies) == 2

    scene.remove_entity(ent1)
    assert len(scene.physics.rigidbodies) == 1

    scene.remove_entity(ent2.id)
    assert len(scene.physics.rigidbodies) == 0
