# Guest To Internal Access Detection Report

Status: generated from validated sample event.

Generated at: 2026-05-16T20:03:16Z

## Summary

Guest-originated traffic attempted to reach an internal MERIDIAN LABS zone and
was represented as denied by the segmentation contract. The validation path
confirmed that the event schema is valid, the event maps to a deny flow, and the
detection rule matches the denied access pattern.

This report is generated from repository sample data. It is not runtime evidence
from a live firewall, network sensor, or container topology.

## Matched Flow

- Flow ID: `D2`
- Source zone: `branch-guest-client`
- Destination zone: `branch-local-service`
- Protocol: `tcp`
- Port: `any`
- Action: `deny`
- Rationale: Guest traffic must not reach restricted branch services by default.

## Matched Detection

- Rule ID: `guest-to-internal-denied`
- Rule name: Guest traffic denied to internal zone
- Severity: medium

## Event Details

- Event ID: `evt-denied-guest-access-001`
- Event type: `network_flow`
- Service: restricted branch service reachability
- Source zone: `branch-guest-client`
- Destination zone: `branch-local-service`
- Action: `deny`

## Severity

Severity is `medium` because guest-to-internal access attempts are a
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
