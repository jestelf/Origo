"""Валидация шейдеров перед сборкой."""

from .. import commands


def register(cli) -> None:
    if cli is not None:
        cli.add_command(
            "validate-shaders",
            commands.validate_shaders,
            help="Проверить шейдеры",
        )
    print("Shader validator plugin loaded")
