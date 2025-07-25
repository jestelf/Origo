"""Отправка уведомлений в редактор о горячих обновлениях."""

from __future__ import annotations

import logging

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("update_notifier")


def notify_update(message: str) -> None:
    """Вывести уведомление об обновлении модуля или ресурса."""
    _logger.info("[HotReload] %s", message)
