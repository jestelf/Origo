from __future__ import annotations

"""Запуск Origo CLI с загрузкой плагинов."""

from argparse import ArgumentParser
from typing import Iterable, Callable, Any

from . import load_plugins


class CLI:
    """Простейший контейнер для команд."""

    def __init__(self) -> None:
        self.parser = ArgumentParser(prog="origo", description="Origo CLI")
        self.subparsers = self.parser.add_subparsers(dest="command")

    def add_command(self, name: str, func: Callable[[Any], None], help: str = "") -> None:
        cmd = self.subparsers.add_parser(name, help=help)
        cmd.set_defaults(func=func)

    def run(self, args: Iterable[str] | None = None) -> None:
        ns = self.parser.parse_args(args)
        if hasattr(ns, "func"):
            ns.func(ns)
        else:
            self.parser.print_help()


def run_cli(argv: Iterable[str] | None = None) -> None:
    """Создаёт CLI, загружает плагины и выполняет выбранную команду."""
    cli = CLI()
    load_plugins(cli)
    cli.run(argv)


if __name__ == "__main__":
    run_cli()
