# Guest To Internal Access Incident Packet

Status: operational sample packet based on repository artifacts.

This scenario models guest-originated traffic attempting to reach an internal
branch service. The current packet uses a validated sample event, a structured
segmentation flow contract, and a generated detection report. No running network
topology currently generates this telemetry.

## Scenario Overview

A guest client in `branch-guest-client` attempts to reach
`branch-local-service`. The segmentation contract says this path must be denied
under flow `D2` because guest traffic must not reach restricted branch services
by default.

## Initial Signal

- Event:
  `detection-engineering/sample-events/denied-guest-access.json`
- Matched flow: `D2`
- Matched detection:
  `detection-engineering/detections/guest-to-internal-denied.yaml`
- Generated report:
  `detection-engineering/reports/guest-to-internal-access-report.md`
- Severity: medium

## Investigation Steps

1. Validate the segmentation contract and sample event with
   `meridian-detect validate`.
2. Confirm the event source zone is `branch-guest-client`.
3. Confirm the event destination zone is `branch-local-service`,
   `branch-employee-client`, or `hq-internal-app`.
4. Confirm the matched flow is a deny rule in
   `network-security/segmentation/flows.yaml`.
5. Confirm the detection rule covers the matched flow ID.
6. Generate or review the detection report.
7. Record whether this is sample data, validation evidence, or runtime telemetry.

## Containment Decision

No emergency containment is required for the current sample because the event is
repository evidence, not runtime telemetry. In a future running topology, the
expected containment decision is to preserve the default-deny guest boundary,
avoid adding broad exceptions, and investigate repeated attempts or policy drift.

## Evidence Links

- Validation output:
  `network-security/segmentation/evidence/validation-output.txt`
- Report generation output:
  `network-security/segmentation/evidence/report-generation-output.txt`
- Analyst notes:
  `incident-response/scenarios/guest-to-internal-access/evidence/analyst-notes.md`
- Investigation timeline:
  `incident-response/scenarios/guest-to-internal-access/evidence/investigation-timeline.md`
- Runbook:
  `incident-response/runbooks/segmentation-violation.md`

## Lessons Learned

- A structured flow contract makes the deny decision reviewable.
- A schema-validated event gives detection logic stable fields to inspect.
- The current signal is operationally useful as a repository workflow, but it
  still needs runtime topology evidence before it can prove network enforcement.
- Future telemetry should add recurrence, source instance, and validation
  command context before raising severity.
