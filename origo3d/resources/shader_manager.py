"""Загрузка и кеширование GLSL-шейдеров с поддержкой горячей пересборки."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
import logging

import moderngl

from hotreload.shader_watcher import watch_shader
from hotreload.hotreloader import HotReloader


class ShaderManager:
    """Компилирует и кеширует программы moderngl."""

    def __init__(self, reloader: HotReloader | None = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.reloader = reloader
        self._programs: Dict[Tuple[int, Path, Path], moderngl.Program] = {}

    def load_program(
        self,
        ctx: moderngl.Context,
        vertex_shader: str | Path,
        fragment_shader: str | Path,
    ) -> moderngl.Program:
        """Загрузить и скомпилировать программу или вернуть из кеша."""
        vert_path = Path(vertex_shader).resolve()
        frag_path = Path(fragment_shader).resolve()
        key = (id(ctx), vert_path, frag_path)
        if key in self._programs:
            return self._programs[key]

        program = self._compile(ctx, vert_path, frag_path)
        self._programs[key] = program

        if self.reloader:
            watch_shader(self.reloader, vert_path, lambda _: self._reload(key, ctx, vert_path, frag_path))
            watch_shader(self.reloader, frag_path, lambda _: self._reload(key, ctx, vert_path, frag_path))

        return program

    def _compile(self, ctx: moderngl.Context, vert_path: Path, frag_path: Path) -> moderngl.Program:
        vert_src = vert_path.read_text(encoding="utf-8")
        frag_src = frag_path.read_text(encoding="utf-8")
        return ctx.program(vertex_shader=vert_src, fragment_shader=frag_src)

    def _reload(self, key: Tuple[int, Path, Path], ctx: moderngl.Context, vert: Path, frag: Path) -> None:
        try:
            program = self._compile(ctx, vert, frag)
            self._programs[key] = program
            self.logger.info("Shader recompiled: %s %s", vert.name, frag.name)
        except Exception as exc:  # pragma: no cover - depends on env
            self.logger.error("Failed to recompile shader: %s", exc)
