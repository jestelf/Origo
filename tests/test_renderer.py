"""Tests for the rendering subsystem."""

"""Tests for the rendering subsystem."""

from origo3d.rendering.renderer import Renderer


def test_camera_mvp_shape():
    renderer = Renderer()
    mvp = renderer.camera.mvp_matrix()
    assert mvp.shape == (4, 4)


def test_renderer_initializes():
    renderer = Renderer()
    # Контекст должен быть создан, а программа скомпилирована
    assert renderer.program is not None
    renderer.render_frame()


def test_model_loaded():
    renderer = Renderer()
    assert renderer.vbo.size > 0

