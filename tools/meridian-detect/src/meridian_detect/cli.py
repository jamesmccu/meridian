"""Command-line interface for MERIDIAN detection engineering workflows."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from meridian_detect import __version__
from meridian_detect.config import get_config
from meridian_detect.validation import (
    DetectionFinding,
    MeridianValidationError,
    detect_guest_to_internal_denied,
    find_matching_deny_flow,
    load_detection_rule,
    load_json,
    load_yaml,
    render_markdown_report,
    validate_event_against_schema,
    validate_flows_contract,
)

DEFAULT_FLOWS = Path("network-security/segmentation/flows.yaml")
DEFAULT_SCHEMA = Path("observability/schemas/meridian-event.schema.json")
DEFAULT_EVENT = Path("detection-engineering/sample-events/denied-guest-access.json")
DEFAULT_RULE = Path("detection-engineering/detections/guest-to-internal-denied.yaml")
DEFAULT_REPORT = Path(
    "detection-engineering/reports/guest-to-internal-access-report.md"
)


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
        help="validate segmentation flows, sample event, and detection match",
    )
    validate_parser.add_argument(
        "--flows",
        type=Path,
        default=DEFAULT_FLOWS,
        help="path to segmentation flows YAML",
    )
    validate_parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="path to Meridian event JSON schema",
    )
    validate_parser.add_argument(
        "--event",
        type=Path,
        default=DEFAULT_EVENT,
        help="path to sample event JSON",
    )
    validate_parser.add_argument(
        "--rule",
        type=Path,
        default=DEFAULT_RULE,
        help="path to detection rule YAML",
    )
    validate_parser.set_defaults(handler=_validate_vertical_slice)

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
        help="generate the guest-to-internal denied access report",
    )
    report_parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REPORT,
        help="report output path",
    )
    report_parser.add_argument(
        "--flows",
        type=Path,
        default=DEFAULT_FLOWS,
        help="path to segmentation flows YAML",
    )
    report_parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="path to Meridian event JSON schema",
    )
    report_parser.add_argument(
        "--event",
        type=Path,
        default=DEFAULT_EVENT,
        help="path to sample event JSON",
    )
    report_parser.add_argument(
        "--rule",
        type=Path,
        default=DEFAULT_RULE,
        help="path to detection rule YAML",
    )
    report_parser.set_defaults(handler=_write_report)

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


def _validate_vertical_slice(args: argparse.Namespace) -> int:
    try:
        finding = _build_finding(args.flows, args.schema, args.event, args.rule)
    except MeridianValidationError as exc:
        print(f"validation failed: {exc}")
        return 1

    print(
        json.dumps(
            {
                "status": "ok",
                "matched_rule": finding.rule_id,
                "matched_flow": finding.flow_id,
                "event_id": finding.event_id,
                "finding": finding.rule_name,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _write_report(args: argparse.Namespace) -> int:
    try:
        finding = _build_finding(args.flows, args.schema, args.event, args.rule)
    except MeridianValidationError as exc:
        print(f"report failed: {exc}")
        return 1

    report = render_markdown_report(finding, datetime.now(UTC))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"wrote report: {args.output}")
    return 0


def _build_finding(
    flows_path: Path, schema_path: Path, event_path: Path, rule_path: Path
) -> DetectionFinding:
    flows_doc = load_yaml(flows_path)
    flows = validate_flows_contract(flows_doc)
    schema = load_json(schema_path)
    event = load_json(event_path)
    validate_event_against_schema(event, schema)
    deny_flow = find_matching_deny_flow(event, flows)
    rule = load_detection_rule(rule_path)
    return detect_guest_to_internal_denied(event, deny_flow, rule)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the meridian-detect CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    return int(args.handler(args))
