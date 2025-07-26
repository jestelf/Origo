from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def collect_crash_stats(log_path: str | Path = "telemetry/events.log") -> Counter:
    """Подсчитывает количество падений по причинам.

    Возвращает Counter, где ключ -- причина падения (поле ``reason``),
    а значение -- число таких событий.
    Если файл отсутствует, возвращается пустой Counter.
    """
    path = Path(log_path)
    stats: Counter[str] = Counter()
    if not path.exists():
        return stats
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event_type") != "crash":
                continue
            reason = str(event.get("reason", "unknown"))
            stats[reason] += 1
    return stats


def main(log_path: str = "telemetry/events.log") -> None:
    stats = collect_crash_stats(log_path)
    print("== Статистика падений ==")
    for reason, count in stats.items():
        print(f"{reason}: {count}")


if __name__ == "__main__":  # pragma: no cover
    main()
