from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from telemetry.crash_frequency import collect_crash_stats


def test_collect_crash_stats(tmp_path: Path) -> None:
    log = tmp_path / "events.log"
    events = [
        {"event_type": "crash", "reason": "segfault"},
        {"event_type": "crash", "reason": "overflow"},
        {"event_type": "crash", "reason": "segfault"},
        {"event_type": "info"},
    ]
    log.write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")

    stats = collect_crash_stats(log)
    assert stats["segfault"] == 2
    assert stats["overflow"] == 1

