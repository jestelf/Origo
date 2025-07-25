from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origo3d.ai.procedural import generate_terrain, generate_level


def test_generate_terrain_shape():
    terrain = generate_terrain()
    assert terrain.shape == (64, 64)
    assert terrain.min() >= 0
    assert terrain.max() <= 1


def test_generate_level_shape():
    level = generate_level()
    assert level.shape == (15, 20)
    # В уровне должны быть стены по краям
    assert (level[0, :] == 1).all()
    assert (level[-1, :] == 1).all()
    assert (level[:, 0] == 1).all()
    assert (level[:, -1] == 1).all()
