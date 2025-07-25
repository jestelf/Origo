"""Тесты для базовой физики."""

from pathlib import Path
import sys

from pyrr import Vector3

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origo3d.scene import Entity, Scene
from origo3d.physics import RigidBody, SphereCollider


def test_rigidbody_motion():
    scene = Scene()
    ent = Entity("ball")
    rb = RigidBody(mass=1.0, collider=SphereCollider(radius=1.0))
    ent.add_component(rb)
    scene.add_entity(ent)

    rb.add_force(Vector3([0.0, 9.81, 0.0]))
    scene.update(1.0)

    assert ent.position.y > 0
