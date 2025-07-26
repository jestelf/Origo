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
    monkeypatch.setattr(env_settings, "_ENV_DIR", cfg_dir / "env")
    env_settings._settings = {}

    settings = env_settings.load()
    assert settings["graphics"]["vsync"] is False
    assert "extra" in settings


def test_env_multiple_files(tmp_path, monkeypatch):
    base_cfg = tmp_path / "config.yaml"
    base_cfg.write_text("graphics:\n  vsync: false\n")

    cfg_dir = tmp_path / "configs"
    env_dir = cfg_dir / "env"
    env_dir.mkdir(parents=True)
    (env_dir / "dev.yaml").write_text("DEBUG: 1\n")
    (env_dir / "local.yaml").write_text("CACHE: 0\n")

    monkeypatch.setattr(env_settings, "_BASE_CONFIG", base_cfg)
    monkeypatch.setattr(env_settings, "_CONFIG_DIR", cfg_dir)
    monkeypatch.setattr(env_settings, "_ENV_DIR", env_dir)
    env_settings._settings = {}

    settings = env_settings.load()
    assert settings["env"]["dev"]["DEBUG"] == 1
    assert settings["env"]["local"]["CACHE"] == 0


def test_missing_base_config(tmp_path, monkeypatch):
    base_cfg = tmp_path / "config.yaml"  # do not create

    cfg_dir = tmp_path / "configs"
    cfg_dir.mkdir()
    (cfg_dir / "graphics.yaml").write_text("api: opengl\n")

    monkeypatch.setattr(env_settings, "_BASE_CONFIG", base_cfg)
    monkeypatch.setattr(env_settings, "_CONFIG_DIR", cfg_dir)
    monkeypatch.setattr(env_settings, "_ENV_DIR", cfg_dir / "env")
    env_settings._settings = {}

    settings = env_settings.load()
    assert settings.get("graphics", {}).get("api") == "opengl"


def test_invalid_yaml(tmp_path, monkeypatch):
    base_cfg = tmp_path / "config.yaml"
    base_cfg.write_text("graphics: [1, 2]\n")

    cfg_dir = tmp_path / "configs"
    cfg_dir.mkdir()
    (cfg_dir / "bad.yaml").write_text("foo: [1, 2\n")

    monkeypatch.setattr(env_settings, "_BASE_CONFIG", base_cfg)
    monkeypatch.setattr(env_settings, "_CONFIG_DIR", cfg_dir)
    monkeypatch.setattr(env_settings, "_ENV_DIR", cfg_dir / "env")
    env_settings._settings = {}

    settings = env_settings.load()
    assert settings.get("bad", {}) == {}
