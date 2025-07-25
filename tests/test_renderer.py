"""Тесты подсистемы рендеринга."""

from __future__ import annotations

import pytest

from origo3d.rendering.renderer import Renderer


def _safe_renderer() -> Renderer:
    """Вернуть экземпляр ``Renderer`` или пропустить тест."""
    try:
        return Renderer()
    except Exception as exc:  # pragma: no cover - зависит от среды
        pytest.skip(f"Renderer init failed: {exc}")


def test_camera_mvp_shape() -> None:
    renderer = _safe_renderer()
    mvp = renderer.camera.mvp_matrix()
    assert mvp.shape == (4, 4)


def test_renderer_initializes() -> None:
    renderer = _safe_renderer()
    assert renderer.program is not None
    renderer.render_frame()


def test_model_loaded() -> None:
    renderer = _safe_renderer()
    assert renderer.vbo.size > 0
