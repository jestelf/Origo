import json
from pathlib import Path
from typing import Iterable, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


EventPos = Tuple[float, float]


def load_error_positions(log_path: str | Path = "telemetry/events.log") -> List[EventPos]:
    """Читает файл событий и извлекает координаты ошибок или падений."""
    path = Path(log_path)
    positions: List[EventPos] = []
    if not path.exists():
        return positions

    with path.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event_type") not in {"crash", "error", "fall"}:
                continue
            if "position" in event and isinstance(event["position"], (list, tuple)):
                pos = event["position"]
                if len(pos) >= 2:
                    positions.append((float(pos[0]), float(pos[1])))
            elif "x" in event and "y" in event:
                positions.append((float(event["x"]), float(event["y"])) )
    return positions


def plot_heatmap(positions: Iterable[EventPos], bins: int = 50, show: bool = True) -> None:
    """Строит тепловую карту по координатам."""
    positions = list(positions)
    if not positions:
        print("Предупреждение: нет данных о падениях или ошибках.")
        return

    xs, ys = zip(*positions)
    heatmap, xedges, yedges = np.histogram2d(xs, ys, bins=bins)

    plt.imshow(heatmap.T, origin="lower", cmap="hot", aspect="auto")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Карта падений/ошибок")
    plt.colorbar(label="Количество")
    if show:
        plt.show()
    else:
        plt.close()


def main(log_path: str = "telemetry/events.log") -> None:
    positions = load_error_positions(log_path)
    plot_heatmap(positions)


if __name__ == "__main__":  # pragma: no cover
    main()
