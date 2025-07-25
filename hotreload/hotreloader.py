from __future__ import annotations

import importlib
from pathlib import Path
from typing import Callable, Dict

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ReloadHandler(FileSystemEventHandler):
    """Обработчик событий файловой системы для перезагрузки."""

    def __init__(self, reloader: "HotReloader") -> None:
        self.reloader = reloader

    def on_modified(self, event) -> None:  # type: ignore[override]
        if not event.is_directory:
            self.reloader.reload_path(Path(event.src_path))

    def on_created(self, event) -> None:  # type: ignore[override]
        if not event.is_directory:
            self.reloader.reload_path(Path(event.src_path))


class HotReloader:
    """Следит за изменениями файлов и обновляет модули и ресурсы."""

    def __init__(self) -> None:
        self.observer = Observer()
        self.modules: Dict[Path, str] = {}
        self.resources: Dict[Path, Callable[[Path], None]] = {}
        self.handler = ReloadHandler(self)

    def watch_module(self, module_name: str) -> None:
        module = importlib.import_module(module_name)
        path = Path(module.__file__).resolve()
        self.modules[path] = module_name
        self.observer.schedule(self.handler, path.parent, recursive=False)

    def watch_resource(self, file: str | Path, on_reload: Callable[[Path], None]) -> None:
        path = Path(file).resolve()
        self.resources[path] = on_reload
        self.observer.schedule(self.handler, path.parent, recursive=False)

    def reload_path(self, path: Path) -> None:
        from editors.update_notifier import notify_update

        if path in self.modules:
            name = self.modules[path]
            importlib.reload(importlib.import_module(name))
            notify_update(f"Модуль {name} был перезагружен")
        elif path in self.resources:
            self.resources[path](path)
            notify_update(f"Ресурс {path.name} был обновлён")

    def start(self) -> None:
        self.observer.start()

    def stop(self) -> None:
        self.observer.stop()
        self.observer.join()
