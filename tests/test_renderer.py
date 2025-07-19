"""Tests for the rendering subsystem."""

from origo3d.rendering.renderer import Renderer


def test_renderer_initializes():
    renderer = Renderer()
    # Контекст должен быть создан, а программа скомпилирована
    assert renderer.program is not None
    renderer.render_frame()

