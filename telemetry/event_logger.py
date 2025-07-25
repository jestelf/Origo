import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict


class EventLogger:
    """Простой логгер игровых событий."""

    def __init__(self, log_path: str | Path = "telemetry/events.log") -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record_event(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Сохраняет событие в файл и возвращает запись."""
        record = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            **data,
        }
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record
