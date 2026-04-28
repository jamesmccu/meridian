"""Tests for meridian_detect.config."""

from meridian_detect.config import get_config


def test_default_quickwit_url():
    config = get_config()
    assert config["quickwit_url"] == "https://quickwit.meridian.local:7280"


def test_default_events_dir():
    config = get_config()
    assert config["events_dir"] == "events/samples"


def test_default_log_level():
    config = get_config()
    assert config["log_level"] == "INFO"


def test_env_override_log_level(monkeypatch):
    monkeypatch.setenv("MERIDIAN_LOG_LEVEL", "DEBUG")

    config = get_config()

    assert config["log_level"] == "DEBUG"


def test_env_override_quickwit_url(monkeypatch):
    monkeypatch.setenv("MERIDIAN_QUICKWIT_URL", "https://quickwit.example.com")

    config = get_config()

    assert config["quickwit_url"] == "https://quickwit.example.com"
