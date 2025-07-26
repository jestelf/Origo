"""Пример плагина тестирования AI."""

from .. import commands


def register(cli) -> None:
    if cli is not None:
        cli.add_command(
            "run-ai-tests",
            commands.run_ai_tests,
            help="Запустить AI тесты",
        )
    print("AI test runner plugin loaded")
