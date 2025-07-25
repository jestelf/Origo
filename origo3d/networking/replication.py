from __future__ import annotations

"""Механизмы репликации состояния объектов."""

from typing import Any, Dict
import asyncio


class ReplicationManager:
    """Хранит и синхронизирует состояние игровых объектов."""

    def __init__(self) -> None:
        self._objects: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def apply_update(self, update: Dict[str, Dict[str, Any]]) -> None:
        """Применить изменения от клиента."""
        async with self._lock:
            for obj_id, state in update.items():
                self._objects[obj_id] = state

    async def merge_state(self, state: Dict[str, Dict[str, Any]]) -> None:
        """Обновить локальное состояние данными с сервера."""
        async with self._lock:
            self._objects.update(state)

    async def snapshot(self) -> Dict[str, Dict[str, Any]]:
        """Вернуть копию текущего состояния."""
        async with self._lock:
            return dict(self._objects)
