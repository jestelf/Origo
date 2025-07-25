"""CLI для управления модами."""

from __future__ import annotations

import argparse

from origo3d.modding.mod_manager import ModManager


def main() -> None:
    parser = argparse.ArgumentParser(description="Управление модами")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="Показать установленные моды")

    install = sub.add_parser("install", help="Скачать мод из облака")
    install.add_argument("name")

    upload = sub.add_parser("upload", help="Выгрузить мод в облако")
    upload.add_argument("name")

    remove = sub.add_parser("remove", help="Удалить мод")
    remove.add_argument("name")

    args = parser.parse_args()

    manager = ModManager()

    if args.cmd == "list":
        for mod in manager.list_installed():
            print(mod)
    elif args.cmd == "install":
        manager.install_from_cloud(args.name)
    elif args.cmd == "upload":
        manager.upload_to_cloud(args.name)
    elif args.cmd == "remove":
        manager.remove_mod(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

