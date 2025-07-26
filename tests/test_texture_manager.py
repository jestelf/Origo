from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origo3d.resources.texture_manager import TextureManager
from origo3d.resources.manifest import AssetManifest
from runtime import env_settings


def _create_image(path: Path, size=(64, 64)) -> None:
    img = Image.new("RGBA", size, (255, 0, 0, 255))
    img.save(path)


def test_texture_load_and_cache(tmp_path: Path) -> None:
    manifest = AssetManifest(tmp_path / "manifest.json")
    manager = TextureManager(manifest)
    img_path = tmp_path / "img.png"
    _create_image(img_path)
    guid = manager.import_texture(img_path)
    tex1 = manager.get(guid)
    tex2 = manager.get(guid)
    assert tex1 is tex2
    assert tex1.size == (64, 64)


def test_mobile_scaling(tmp_path: Path, monkeypatch) -> None:
    manifest = AssetManifest(tmp_path / "manifest.json")
    manager = TextureManager(manifest)
    img_path = tmp_path / "img.png"
    _create_image(img_path, (128, 128))
    monkeypatch.setattr(env_settings, "mobile_mode", lambda: True)
    monkeypatch.setattr(env_settings, "get", lambda s=None, default=None: {"texture_resolution": 32} if s == "graphics" else {})
    guid = manager.import_texture(img_path)
    tex = manager.get(guid)
    assert tex.size[0] <= 32 and tex.size[1] <= 32
