"""Сбор статистики по сцене."""

from .. import commands


def register(cli) -> None:
    if cli is not None:
        cli.add_command(
            "scene-stats",
            commands.scene_stats,
            help="Вывести статистику сцен",
        )
    print("Scene stats plugin loaded")
