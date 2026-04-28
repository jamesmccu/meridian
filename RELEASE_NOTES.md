# Release Notes

Milestone summaries for MERIDIAN. For detailed history, see
[CHANGELOG.md](./CHANGELOG.md).

## Unreleased — MERIDIAN v2 Repositioning

Focus: narrow MERIDIAN from a broad homelab/SRE platform into a Kubernetes runtime
detection engineering project.

- Rewrote README around detection engineering.
- Rewrote active architecture docs for the target Falco -> Vector -> Quickwit ->
  Python enrichment flow.
- Archived broad platform, cloud, GitOps, IaC, and static-site planning docs in
  the `meridian-v1-platform-archive` Git tag and removed them from the default
  branch.
- Reframed `security/README.md` so detections should live in this repository.
- Kept existing Quickwit, Vector, Trivy, and Python quality checks as useful v2
  building blocks.
- Clarified that Falco rules, synthetic tests, MITRE mapping, and enrichment are
  planned v2 work, not currently implemented on main.

## Current Baseline

Currently configured:

- Trivy filesystem, image, and config scanning.
- Python linting, type checking, and tests.
- YAML validation.
- Quickwit configuration.
- Vector and Fluent Bit configuration.
- Legacy Docker Compose lab.
- Minimal `meridian-core` diagnostics package.

Not currently implemented on main:

- Falco runtime rules.
- Kubernetes deployment profile.
- Synthetic adversary tests.
- MITRE ATT&CK mapping.
- Python detection enrichment.
- Alert sink or dashboard.
