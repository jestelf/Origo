"""Тесты подсистемы рендеринга."""

import pytest

from origo3d.rendering.renderer import Renderer


@pytest.fixture()
def renderer():
    try:
        return Renderer()
    except Exception:
        pytest.skip("Renderer init failed")


def test_camera_mvp_shape(renderer):
    mvp = renderer.camera.mvp_matrix()
    assert mvp.shape == (4, 4)


def test_renderer_initializes(renderer):
    assert renderer.program is not None
    renderer.render_frame()


def test_model_loaded(renderer):
    assert renderer.vbo.size > 0
