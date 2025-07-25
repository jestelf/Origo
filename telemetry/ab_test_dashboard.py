from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def load_variant_counts(log_path: str | Path = "telemetry/events.log") -> Counter:
    path = Path(log_path)
    counter: Counter[str] = Counter()
    if not path.exists():
        return counter
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            event = json.loads(line)
            if event.get("event_type") == "ab_test_variant":
                counter[event.get("variant", "")] += 1
    return counter


def main(log_path: str = "telemetry/events.log") -> None:
    counts = load_variant_counts(log_path)
    print("A/B статистика:")
    for variant, count in counts.items():
        print(f"{variant}: {count}")


if __name__ == "__main__":  # pragma: no cover
    main()
