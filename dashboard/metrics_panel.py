from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def collect_metrics(log_path: str | Path = "telemetry/events.log") -> Counter:
    path = Path(log_path)
    metrics: Counter[str] = Counter()
    if not path.exists():
        return metrics
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            event = json.loads(line)
            metrics[event["event_type"]] += 1
    return metrics


def main(log_path: str = "telemetry/events.log") -> None:
    metrics = collect_metrics(log_path)
    print("== Метрики ==")
    for event, count in metrics.items():
        print(f"{event}: {count}")


if __name__ == "__main__":  # pragma: no cover
    main()
