from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from telemetry.crash_heatmap import load_error_positions, plot_heatmap


def test_load_error_positions(tmp_path: Path) -> None:
    log = tmp_path / "events.log"
    events = [
        {"event_type": "crash", "position": [1, 2, 3]},
        {"event_type": "error", "x": 4, "y": 5},
        {"event_type": "other", "x": 0, "y": 0},
    ]
    log.write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")

    positions = load_error_positions(log)
    assert positions == [(1.0, 2.0), (4.0, 5.0)]


def test_plot_heatmap_no_data(capsys) -> None:
    plot_heatmap([], show=False)
    captured = capsys.readouterr()
    assert "Предупреждение" in captured.out
