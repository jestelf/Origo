from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from telemetry.event_logger import EventLogger
from telemetry.ab_test_manager import ABTestManager


def test_event_recording(tmp_path: Path) -> None:
    log_file = tmp_path / "events.log"
    logger = EventLogger(log_file)
    logger.record_event("game_started", {"user": "1"})
    assert log_file.exists()
    assert log_file.read_text().count("game_started") == 1


def test_ab_assignment() -> None:
    manager = ABTestManager(["A", "B"])
    variant = manager.assign_variant("user1")
    assert variant in ("A", "B")
    assert manager.summary()[variant] == 1
