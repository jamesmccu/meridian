"""Tests for meridian_core.config."""

from meridian_core.config import get_config


def test_default_vault_addr():
    config = get_config()
    assert config["vault_addr"] == "https://vault.meridian.local:8200"


def test_default_log_level():
    config = get_config()
    assert config["log_level"] == "INFO"


def test_env_override_log_level(monkeypatch):
    monkeypatch.setenv("MERIDIAN_LOG_LEVEL", "DEBUG")

    config = get_config()

    assert config["log_level"] == "DEBUG"


def test_env_override_vault_addr(monkeypatch):
    monkeypatch.setenv("MERIDIAN_VAULT_ADDR", "https://vault.prod.example.com:8200")

    config = get_config()

    assert config["vault_addr"] == "https://vault.prod.example.com:8200"
