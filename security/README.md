# Security

This directory contains active security tooling for MERIDIAN.

Current content:

- `trivy/` — CI vulnerability and configuration scanning.

Planned MERIDIAN v2 content:

- Falco runtime detection rules.
- Detection metadata and MITRE ATT&CK mappings.
- Synthetic detection validation tests.
- Event enrichment and reporting examples.

Runtime detections should live in this repository so reviewers can inspect the
rule logic, test inputs, sample events, and validation evidence together.
