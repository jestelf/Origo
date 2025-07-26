from __future__ import annotations

"""Базовые команды CLI Origo."""

from pathlib import Path
import subprocess

import moderngl


def _has_glslang() -> bool:
    """Проверяет наличие утилиты glslangValidator."""
    try:
        subprocess.run(
            ["glslangValidator", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except Exception:
        return False


def _validate_with_glslang(path: Path) -> tuple[bool, str]:
    """Компилирует шейдер через glslangValidator."""
    res = subprocess.run(
        ["glslangValidator", str(path)], capture_output=True, text=True
    )
    return res.returncode == 0, (res.stdout + res.stderr).strip()


def _validate_with_mgl(path: Path) -> tuple[bool, str]:
    """Пробует скомпилировать шейдер средствами ModernGL."""
    src = path.read_text()
    ctx = moderngl.create_standalone_context()
    errors = []
    for fn in (ctx.vertex_shader, ctx.fragment_shader, ctx.compute_shader):
        try:
            fn(src)
            return True, ""
        except Exception as exc:  # pragma: no cover - зависит от реализации
            errors.append(str(exc))
    return False, " | ".join(errors)


def validate_shaders(_args) -> None:
    """Проверка корректности шейдеров."""
    shader_dir = Path("assets/shaders")
    shaders = list(shader_dir.glob("*.glsl"))
    if not shaders:
        print(f"Шейдеры не найдены в {shader_dir}")
        return

    use_glslang = _has_glslang()
    ok: list[Path] = []
    failed: list[tuple[Path, str]] = []

    for shader in shaders:
        if use_glslang:
            success, log = _validate_with_glslang(shader)
        else:
            success, log = _validate_with_mgl(shader)

        if success:
            ok.append(shader)
        else:
            failed.append((shader, log))

    print("Успешно скомпилированы:")
    for path in ok:
        print(f"  {path}")

    if failed:
        print("Проблемные шейдеры:")
        for path, msg in failed:
            print(f"  {path}: {msg}")
    else:
        print("Ошибок не найдено")


def scene_stats(_args) -> None:
    """Сбор статистики по сценам."""
    print("Gathering scene statistics...")


def check_textures(_args) -> None:
    """Проверка текстур на корректность."""
    print("Checking textures...")


def run_ai_tests(_args) -> None:
    """Запуск тестов ИИ."""
    print("Running AI tests...")
