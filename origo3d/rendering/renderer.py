"""Minimal rendering context using moderngl."""

from __future__ import annotations

from typing import Tuple

import moderngl


class Renderer:
    """Create a rendering context and clear the screen."""

    def __init__(self) -> None:
        # ``moderngl.create_context`` uses the active OpenGL context
        self.ctx = moderngl.create_context()
        self.clear_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)

    def render_frame(self) -> None:
        """Clear the screen with the configured color."""
        r, g, b, a = self.clear_color
        self.ctx.clear(r, g, b, a)

