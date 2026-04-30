# Changelog

All notable changes to MERIDIAN are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

### Changed
- Pivoted project positioning from MERIDIAN v2 Kubernetes runtime detection to
  MERIDIAN LABS, a distributed office security lab for branch, HQ, and cloud
  security architecture practice.
- Rewrote README and architecture documentation around segmentation, secure
  connectivity, host hardening, telemetry, detection, and policy-as-code.
- Added threat model, roadmap, interview positioning, and design-decision docs
  to explain the pivot and preserve useful v2 material.
- Added initial lab module scaffolds, learning tasks, and diagrams placeholder
  for the MERIDIAN LABS roadmap.
- Added the first Lab 01 network segmentation flow table to define zones,
  allowed flows, denied flows, validation plan, assumptions, and local-lab
  limitations before implementation.
- Reframed lab folders and documentation around problem-driven security
  engineering labs: segmentation and trust boundaries, secure connectivity and
  remote access, hardening and baseline enforcement, telemetry/detection/
  response, and policy-as-code validation.
- Renamed `meridian-core` to `meridian-detect` and added a CLI scaffold for
  current config output and planned detection workflow commands.
- Removed archived platform-era material from the default branch after tagging it
  as `meridian-v1-platform-archive`.
- Previously repositioned MERIDIAN as a Kubernetes runtime detection engineering
  project before the broader MERIDIAN LABS pivot.
- Rewrote README around the v2 detection workflow.
- Rewrote active architecture and learning-map docs.
- Rewrote `security/README.md` to make this repository the future home for
  detection logic, metadata, sample events, and validation evidence.
- Updated `STRUCTURE.md` for the narrowed v2 scope.
- Updated Python tooling wording to avoid broad observability/platform claims.

### Retained
- MERIDIAN v2 observability, Trivy, CI, and `meridian-detect` work as future
  telemetry/detection lab inputs.
- Trivy CI scanning.
- Python lint, type check, and test workflow.
- YAML validation.
- Quickwit, Vector, and Fluent Bit configuration as useful event-pipeline
  building blocks.
- Legacy Compose lab for reference.

### Planned
- First validated segmentation implementation and evidence file.
- Secure connectivity and remote-access exercise.
- Host hardening and baseline-enforcement exercise.
- Telemetry, detection, and response exercise using retained v2 assets.
- Policy-as-code and automated-validation exercise.
