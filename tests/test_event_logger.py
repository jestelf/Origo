from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from telemetry.event_logger import EventLogger


def test_record_event_creates_file(tmp_path: Path) -> None:
    log_file = tmp_path / "events.log"
    logger = EventLogger(log_file)
    logger.record_event("game_started", {"user": "42"})

    assert log_file.exists()
    text = log_file.read_text(encoding="utf-8")
    assert "game_started" in text


def test_event_json_contents(tmp_path: Path) -> None:
    log_file = tmp_path / "events.log"
    logger = EventLogger(log_file)
    logger.record_event("level_completed", {"user": "7"})

    data = log_file.read_text(encoding="utf-8").splitlines()[0]
    event = json.loads(data)

    assert event["event_type"] == "level_completed"
    assert event["user"] == "7"
    assert "timestamp" in event
