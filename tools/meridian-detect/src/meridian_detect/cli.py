"""Command-line interface for MERIDIAN detection engineering workflows."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from meridian_detect import __version__
from meridian_detect.config import get_config


def build_parser() -> argparse.ArgumentParser:
    """Build the meridian-detect argument parser."""
    parser = argparse.ArgumentParser(
        prog="meridian-detect",
        description=(
            "Detection engineering CLI scaffold for MERIDIAN. "
            "Current commands expose configuration and planned workflow entry points."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"meridian-detect {__version__}",
    )

    subcommands = parser.add_subparsers(dest="command")

    config_parser = subcommands.add_parser(
        "config",
        help="print effective non-secret detection tooling configuration",
    )
    config_parser.set_defaults(handler=_print_config)

    validate_parser = subcommands.add_parser(
        "validate",
        help="placeholder for future detection validation",
    )
    validate_parser.add_argument(
        "--events",
        default=None,
        help="future path to sample events used for validation",
    )
    validate_parser.set_defaults(handler=_not_implemented)

    enrich_parser = subcommands.add_parser(
        "enrich",
        help="placeholder for future event enrichment",
    )
    enrich_parser.add_argument(
        "--input",
        default=None,
        help="future input event file or stream",
    )
    enrich_parser.set_defaults(handler=_not_implemented)

    report_parser = subcommands.add_parser(
        "report",
        help="placeholder for future detection report generation",
    )
    report_parser.add_argument(
        "--output",
        default=None,
        help="future output report path",
    )
    report_parser.set_defaults(handler=_not_implemented)

    return parser


def _print_config(_args: argparse.Namespace) -> int:
    print(json.dumps(get_config(), indent=2, sort_keys=True))
    return 0


def _not_implemented(args: argparse.Namespace) -> int:
    print(
        f"meridian-detect {args.command}: placeholder only. "
        "This workflow is planned but not implemented yet."
    )
    return 2


def main(argv: Sequence[str] | None = None) -> int:
    """Run the meridian-detect CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    return int(args.handler(args))
