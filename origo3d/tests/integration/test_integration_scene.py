from __future__ import annotations

from origo3d.rendering.camera import Camera


def test_camera_matrix_shape() -> None:
    cam = Camera()
    mvp = cam.mvp_matrix()
    assert mvp.shape == (4, 4)
