"""Проверка корректности текстур."""

from .. import commands


def register(cli) -> None:
    if cli is not None:
        cli.add_command(
            "check-textures",
            commands.check_textures,
            help="Проверить текстуры",
        )
    print("Texture checker plugin loaded")
