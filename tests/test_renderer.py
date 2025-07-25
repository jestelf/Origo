"""Тесты подсистемы рендеринга."""

import pytest
from origo3d.rendering.renderer import Renderer


def _safe_renderer(**kwargs) -> Renderer:
    """
    Попробовать создать Renderer с переданными параметрами,
    иначе — пропустить тест.
    """
    try:
        return Renderer(**kwargs)
    except Exception as exc:  # pragma: no cover - зависит от окружения
        pytest.skip(f"Renderer init failed: {exc}")


def test_camera_mvp_shape() -> None:
    renderer = _safe_renderer()
    mvp = renderer.camera.mvp_matrix()
    assert mvp.shape == (4, 4)


def test_renderer_initializes() -> None:
    renderer = _safe_renderer()
    assert renderer.program is not None
    # просто должен отрисоваться без ошибок
    renderer.render_frame()


def test_model_loaded() -> None:
    renderer = _safe_renderer()
    assert renderer.vbo.size > 0


def test_vulkan_backend_stub() -> None:
    """
    Проверка бэкенда Vulkan (если он доступен в вашей сборке).
    """
    renderer = _safe_renderer(api="vulkan")
    renderer.render_frame()
    assert renderer.camera is not None
