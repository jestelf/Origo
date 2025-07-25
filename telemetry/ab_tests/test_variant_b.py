from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from telemetry.event_logger import EventLogger
from dashboard.metrics_panel import collect_metrics


def test_metrics_collection(tmp_path: Path) -> None:
    log_file = tmp_path / "events.log"
    logger = EventLogger(log_file)
    logger.record_event("level_completed", {"user": "1"})
    metrics = collect_metrics(log_file)
    assert metrics["level_completed"] == 1
