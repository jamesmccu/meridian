"""
config.py — Centralized configuration for the Meridian platform.

All tools in the Meridian project call get_config() instead of calling
os.getenv() directly. Defaults point to internal DNS names used across
the platform. Any value can be overridden by setting the corresponding
environment variable before the function is called.
"""
import os


def get_config() -> dict:
    """Read platform config from environment variables with sensible defaults."""
    return {
        # Vault — secrets management (AWS, KMS auto-unseal)
        "vault_addr":           os.getenv("MERIDIAN_VAULT_ADDR",           "https://vault.meridian.local:8200"),
        "vault_cacert":         os.getenv("MERIDIAN_VAULT_CACERT",         "/certs/rootCA.pem"),

        # VictoriaMetrics — long-term metrics storage (GCP)
        "victoriametrics_url":  os.getenv("MERIDIAN_VICTORIAMETRICS_URL",  "https://victoriametrics.meridian.local:8428"),

        # Quickwit — log indexing and search (GCP)
        "quickwit_url":         os.getenv("MERIDIAN_QUICKWIT_URL",         "https://quickwit.meridian.local:7280"),

        # General
        "log_level":            os.getenv("MERIDIAN_LOG_LEVEL",            "INFO"),
    }
