from __future__ import annotations

from pathlib import Path

from runtime import env_settings


def test_load_custom_config(tmp_path, monkeypatch):
    base_cfg = tmp_path / "config.yaml"
    base_cfg.write_text("graphics:\n  vsync: false\n")
    cfg_dir = tmp_path / "configs"
    cfg_dir.mkdir()
    (cfg_dir / "extra.yaml").write_text("value: 1\n")

    monkeypatch.setattr(env_settings, "_BASE_CONFIG", base_cfg)
    monkeypatch.setattr(env_settings, "_CONFIG_DIR", cfg_dir)

    settings = env_settings.load()
    assert settings["graphics"]["vsync"] is False
    assert "extra" in settings
