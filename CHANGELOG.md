# Changelog

All notable changes to MERIDIAN are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

### Changed
- Removed archived platform-era material from the default branch after tagging it
  as `meridian-v1-platform-archive`.
- Repositioned MERIDIAN as a Kubernetes runtime detection engineering project.
- Rewrote README around the v2 detection workflow.
- Rewrote active architecture and learning-map docs.
- Rewrote `security/README.md` to make this repository the future home for
  detection logic, metadata, sample events, and validation evidence.
- Updated `STRUCTURE.md` for the narrowed v2 scope.
- Updated `meridian-core` wording to avoid broad observability/platform claims.

### Retained
- Trivy CI scanning.
- Python lint, type check, and test workflow.
- YAML validation.
- Quickwit, Vector, and Fluent Bit configuration as useful event-pipeline
  building blocks.
- Legacy Compose lab for reference.

### Planned
- Falco runtime rule set.
- Detection catalog schema.
- Sample Falco events.
- Synthetic detection validation tests.
- MITRE ATT&CK mapping.
- Python event enrichment and report output.
