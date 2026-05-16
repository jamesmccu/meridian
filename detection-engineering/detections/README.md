# Detections

This directory will hold MERIDIAN LABS detection contracts and detection logic.

Current state: scaffold only. No production detection rules are implemented yet.

## Initial Detection Ideas

- Guest traffic attempts to reach employee or branch-service zones.
- Branch local service attempts to initiate traffic back to employee systems.
- Branch client attempts to reach telemetry management surfaces.
- Unexpected branch-to-branch reachability appears.

Detection content should reference structured flow IDs from
`network-security/segmentation/flows.yaml` and sample events from
`detection-engineering/sample-events/`.
