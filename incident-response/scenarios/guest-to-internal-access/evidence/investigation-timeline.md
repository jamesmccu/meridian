# Investigation Timeline

Scenario: guest-to-internal-access.

| Time | Step | Result |
|---|---|---|
| T+00 | Initial signal reviewed. | Sample event shows guest source zone and branch-service destination zone. |
| T+02 | Event schema validated. | Required event fields are present and accepted by the Meridian event schema. |
| T+04 | Flow contract reviewed. | Event maps to deny flow `D2` in `network-security/segmentation/flows.yaml`. |
| T+06 | Detection rule applied. | Rule `guest-to-internal-denied` matches the event and deny flow. |
| T+08 | Report generated. | Report written to `detection-engineering/reports/guest-to-internal-access-report.md`. |
| T+10 | Containment decision recorded. | No emergency containment for sample data; preserve default-deny design. |

## Timeline Notes

Times are relative because this is an operational sample packet, not a live
incident. Replace relative times with observed timestamps once runtime telemetry
exists.
