"""Centralized configuration for MERIDIAN diagnostics."""
import os


def get_config() -> dict[str, str]:
    """Read platform config from environment variables with sensible defaults."""
    return {
        # Legacy lab services. These defaults are retained until the v2 detection
        # pipeline replaces the earlier platform configuration.
        "vault_addr": os.getenv(
            "MERIDIAN_VAULT_ADDR",
            "https://vault.meridian.local:8200",
        ),
        "vault_cacert": os.getenv(
            "MERIDIAN_VAULT_CACERT",
            "/certs/rootCA.pem",
        ),

        "victoriametrics_url": os.getenv(
            "MERIDIAN_VICTORIAMETRICS_URL",
            "https://victoriametrics.meridian.local:8428",
        ),
        "quickwit_url": os.getenv(
            "MERIDIAN_QUICKWIT_URL",
            "https://quickwit.meridian.local:7280",
        ),

        # General
        "log_level": os.getenv("MERIDIAN_LOG_LEVEL", "INFO"),
    }
