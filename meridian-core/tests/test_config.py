"""Smoke tests for MeridianConfig."""

import pytest
from meridian_core.config import MeridianConfig


def test_default_config() -> None:
    config = MeridianConfig()
    assert config.vault_addr == "https://vault.meridian.local:8200"
    assert config.log_level == "INFO"


def test_config_override() -> None:
    config = MeridianConfig(log_level="DEBUG")
    assert config.log_level == "DEBUG"
