"""Centralized configuration for MERIDIAN detection tooling."""

import os


def get_config() -> dict[str, str]:
    """Read detection-tool config from environment variables."""
    return {
        "quickwit_url": os.getenv(
            "MERIDIAN_QUICKWIT_URL",
            "https://quickwit.meridian.local:7280",
        ),
        "events_dir": os.getenv("MERIDIAN_EVENTS_DIR", "events/samples"),
        "reports_dir": os.getenv("MERIDIAN_REPORTS_DIR", "reports"),
        "log_level": os.getenv("MERIDIAN_LOG_LEVEL", "INFO"),
    }
