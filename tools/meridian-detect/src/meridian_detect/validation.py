"""Validation and detection helpers for MERIDIAN LABS vertical slices."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


class MeridianValidationError(ValueError):
    """Raised when a MERIDIAN validation contract fails."""


@dataclass(frozen=True)
class DetectionFinding:
    """Minimal detection finding produced from a validated sample event."""

    rule_id: str
    rule_name: str
    severity: str
    event_id: str
    event_type: str
    flow_id: str
    source_zone: str
    destination_zone: str
    protocol: str
    port: str
    action: str
    service: str
    rationale: str


REQUIRED_FLOW_FIELDS = {
    "id",
    "source_zone",
    "destination_zone",
    "protocol",
    "port",
    "action",
    "rationale",
    "telemetry_required",
    "validation_status",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise MeridianValidationError(f"{path} must contain a JSON object")
    return data


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML object from disk."""
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise MeridianValidationError(f"{path} must contain a YAML object")
    return data


def validate_flows_contract(flows_doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate the segmentation flow contract and return flow records."""
    zones = flows_doc.get("zones")
    flows = flows_doc.get("flows")
    if not isinstance(zones, list) or not zones:
        raise MeridianValidationError("flows.yaml must define at least one zone")
    if not isinstance(flows, list) or not flows:
        raise MeridianValidationError("flows.yaml must define at least one flow")

    zone_ids = {
        zone.get("id")
        for zone in zones
        if isinstance(zone, dict) and isinstance(zone.get("id"), str)
    }
    if not zone_ids:
        raise MeridianValidationError("flows.yaml zones must include string ids")

    flow_ids: set[str] = set()
    for flow in flows:
        if not isinstance(flow, dict):
            raise MeridianValidationError("each flow must be a mapping")
        missing = REQUIRED_FLOW_FIELDS - flow.keys()
        if missing:
            flow_id = flow.get("id", "<unknown>")
            raise MeridianValidationError(
                f"flow {flow_id} missing required fields: {sorted(missing)}"
            )
        if flow["id"] in flow_ids:
            raise MeridianValidationError(f"duplicate flow id: {flow['id']}")
        flow_ids.add(str(flow["id"]))
        if flow["action"] not in {"allow", "deny"}:
            raise MeridianValidationError(
                f"flow {flow['id']} action must be allow or deny"
            )
        if not isinstance(flow["telemetry_required"], bool):
            raise MeridianValidationError(
                f"flow {flow['id']} telemetry_required must be boolean"
            )
        for field in ("source_zone", "destination_zone"):
            value = flow[field]
            if value not in zone_ids and value not in {"branch-a-zones"}:
                raise MeridianValidationError(
                    f"flow {flow['id']} references unknown {field}: {value}"
                )

    return flows


def validate_event_against_schema(
    event: dict[str, Any], schema: dict[str, Any]
) -> None:
    """Validate the sample event against the local JSON schema subset."""
    required = schema.get("required", [])
    if not isinstance(required, list):
        raise MeridianValidationError("event schema required must be a list")
    missing = [field for field in required if field not in event]
    if missing:
        raise MeridianValidationError(f"event missing required fields: {missing}")

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise MeridianValidationError("event schema properties must be a mapping")

    if schema.get("additionalProperties") is False:
        extra = sorted(set(event) - set(properties))
        if extra:
            raise MeridianValidationError(f"event has unsupported fields: {extra}")

    for field, value in event.items():
        rules = properties.get(field)
        if isinstance(rules, dict) and "enum" in rules and value not in rules["enum"]:
            raise MeridianValidationError(f"event field {field} has invalid value")

    port = event.get("port")
    if isinstance(port, int) and not 1 <= port <= 65535:
        raise MeridianValidationError("event port integer must be 1-65535")
    if isinstance(port, str) and port not in {"any", "management"}:
        raise MeridianValidationError("event port string must be any or management")
    if port is not None and not isinstance(port, int | str):
        raise MeridianValidationError("event port must be integer or string")

    timestamp = event.get("timestamp")
    if isinstance(timestamp, str):
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise MeridianValidationError("event timestamp must be date-time") from exc


def find_matching_deny_flow(
    event: dict[str, Any], flows: list[dict[str, Any]]
) -> dict[str, Any]:
    """Return the deny flow matching a sample network event."""
    for flow in flows:
        if flow["action"] != "deny":
            continue
        if event.get("source_zone") != flow["source_zone"]:
            continue
        if event.get("destination_zone") != flow["destination_zone"]:
            continue
        if not _field_matches(event.get("protocol"), flow["protocol"]):
            continue
        if not _field_matches(event.get("port"), flow["port"]):
            continue
        if event.get("flow_id") and event["flow_id"] != flow["id"]:
            continue
        return flow
    raise MeridianValidationError("sample event does not match a deny flow")


def load_detection_rule(path: Path) -> dict[str, Any]:
    """Load and minimally validate a detection rule contract."""
    rule = load_yaml(path)
    required = {"id", "name", "severity", "match", "finding"}
    missing = required - rule.keys()
    if missing:
        raise MeridianValidationError(
            f"detection rule missing required fields: {sorted(missing)}"
        )
    if not isinstance(rule["match"], dict):
        raise MeridianValidationError("detection rule match must be a mapping")
    return rule


def detect_guest_to_internal_denied(
    event: dict[str, Any], deny_flow: dict[str, Any], rule: dict[str, Any]
) -> DetectionFinding:
    """Apply the guest-to-internal denied access detection rule."""
    match = rule["match"]
    destinations = match.get("destination_zones")
    if not isinstance(destinations, list):
        raise MeridianValidationError("detection rule destination_zones must be a list")
    if event.get("source_zone") != match.get("source_zone"):
        raise MeridianValidationError("event does not match detection source zone")
    if event.get("action") != match.get("action"):
        raise MeridianValidationError("event does not match detection action")
    if event.get("destination_zone") not in destinations:
        raise MeridianValidationError("event does not match detection destination zone")
    if deny_flow["id"] not in match.get("flow_ids", []):
        raise MeridianValidationError("matched deny flow is not covered by rule")

    return DetectionFinding(
        rule_id=str(rule["id"]),
        rule_name=str(rule["name"]),
        severity=str(rule["severity"]),
        event_id=str(event["event_id"]),
        event_type=str(event["event_type"]),
        flow_id=str(deny_flow["id"]),
        source_zone=str(event["source_zone"]),
        destination_zone=str(event["destination_zone"]),
        protocol=str(event.get("protocol", "unknown")),
        port=str(event.get("port", "unknown")),
        action=str(event["action"]),
        service=str(event["service"]),
        rationale=str(deny_flow["rationale"]),
    )


def render_markdown_report(finding: DetectionFinding, generated_at: datetime) -> str:
    """Render an operational Markdown detection report."""
    generated = generated_at.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""# Guest To Internal Access Detection Report

Status: generated from validated sample event.

Generated at: {generated}

## Summary

Guest-originated traffic attempted to reach an internal MERIDIAN LABS zone and
was represented as denied by the segmentation contract. The validation path
confirmed that the event schema is valid, the event maps to a deny flow, and the
detection rule matches the denied access pattern.

This report is generated from repository sample data. It is not runtime evidence
from a live firewall, network sensor, or container topology.

## Matched Flow

- Flow ID: `{finding.flow_id}`
- Source zone: `{finding.source_zone}`
- Destination zone: `{finding.destination_zone}`
- Protocol: `{finding.protocol}`
- Port: `{finding.port}`
- Action: `{finding.action}`
- Rationale: {finding.rationale}

## Matched Detection

- Rule ID: `{finding.rule_id}`
- Rule name: {finding.rule_name}
- Severity: {finding.severity}

## Event Details

- Event ID: `{finding.event_id}`
- Event type: `{finding.event_type}`
- Service: {finding.service}
- Source zone: `{finding.source_zone}`
- Destination zone: `{finding.destination_zone}`
- Action: `{finding.action}`

## Severity

Severity is `{finding.severity}` because guest-to-internal access attempts are a
segmentation-boundary signal. In this sample, the action is denied, so the
primary operational concern is verification, monitoring, and policy integrity
rather than emergency containment.

## Expected Response

1. Confirm the event is tied to the expected denied flow.
2. Verify no matching allowed rule permits the same source and destination path.
3. Check whether repeated events suggest a misconfigured guest client, policy
   probing, or a test artifact.
4. Preserve the validation output and report as scenario evidence.
5. Update the scenario notes if additional telemetry fields are needed.

## False-Positive Considerations

- The event may be intentionally generated sample data.
- A service or zone label may be incorrect in the sample event.
- A future topology could deny the path correctly while still producing noisy
  repeated events from benign guest behavior.
- This report does not prove packet-level enforcement because no runtime network
  topology is attached yet.

## Follow-Up Hardening Actions

- Keep guest networks default-deny toward employee, branch-service, and HQ
  internal zones.
- Add validation evidence once a real topology generates denied-flow telemetry.
- Add rate or recurrence context before treating repeated denials as higher
  severity.
- Review management-surface exposure separately from ordinary service access.

## Evidence Links

- Scenario: `incident-response/scenarios/guest-to-internal-access/README.md`
- Runbook: `incident-response/runbooks/segmentation-violation.md`
- Flow contract: `network-security/segmentation/flows.yaml`
- Sample event: `detection-engineering/sample-events/denied-guest-access.json`
- Validation evidence:
  `network-security/segmentation/evidence/validation-output.txt`
- Report-generation evidence:
  `network-security/segmentation/evidence/report-generation-output.txt`
"""


def _field_matches(event_value: object, rule_value: object) -> bool:
    return rule_value == "any" or event_value == rule_value
