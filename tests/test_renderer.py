"""Tests for the rendering subsystem."""

from origo3d.rendering.renderer import Renderer

def test_camera_mvp_shape():
    renderer = Renderer()
    mvp = renderer.camera.mvp_matrix()
    assert mvp.shape == (4, 4)


def test_renderer_initializes():
    renderer = Renderer()
    assert renderer.program is not None
    renderer.render_frame()


def test_model_loaded():
    renderer = Renderer()
    assert renderer.vbo.size > 0


def test_vulkan_backend_stub():
    renderer = Renderer(api="vulkan")
    renderer.render_frame()
    assert renderer.camera is not None

