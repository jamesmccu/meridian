# Learning Map

MERIDIAN v2 is optimized for detection engineering and Kubernetes runtime
security.

## Primary Skill Targets

| Area | MERIDIAN v2 Practice |
|---|---|
| Detection engineering | Write, test, tune, and document runtime detections. |
| Kubernetes security | Exercise detections against Kubernetes workload behavior. |
| Linux/runtime security | Reason about process, file, network, and container events. |
| Security automation | Enrich events and produce findings with Python. |
| Security data engineering | Route structured events into a searchable backend. |
| Network/security systems thinking | Detect suspicious egress, tooling, and lateral movement patterns. |

## What To Build Personally

The most valuable learning work should be done by the repo owner:

- Detection catalog design.
- Falco rule logic.
- Synthetic triggers.
- Sample event capture.
- MITRE ATT&CK mapping.
- Python enrichment and correlation.
- False-positive analysis.

## What Can Be Mechanical Cleanup

Lower-learning-value work:

- Moving legacy docs.
- Rewriting old platform positioning.
- Updating repository structure docs.
- Keeping CI and public hygiene clean.

## Proof Of Competence

A strong MERIDIAN v2 detection should show the full loop:

```text
rule -> trigger -> event -> enrichment -> ATT&CK mapping -> finding -> validation
```

One complete validated detection is more valuable than many untested tools.
