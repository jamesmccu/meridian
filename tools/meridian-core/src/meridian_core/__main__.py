"""Command-line entry point for meridian-core diagnostics."""

import json

from meridian_core.config import get_config


def main() -> None:
    """Print the effective non-secret Meridian configuration."""
    print(json.dumps(get_config(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
