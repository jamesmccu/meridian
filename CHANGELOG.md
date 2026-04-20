# Changelog

All notable changes to the Meridian Platform are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

### Planned
- GCP observability plane — migrate VictoriaMetrics, Quickwit, and Grafana to e2-micro
- Falco eBPF runtime security monitoring
- OPA/Gatekeeper Kubernetes admission control
- ArgoCD GitOps control plane (App of Apps pattern)
- Linkerd service mesh with mTLS
- KMS auto-unseal for Vault
- stagegrid-tickets FastAPI service (first StageGrid service)

---

## [0.3.0] — 2026-04

### Changed
- Reconciled STRUCTURE.md and README directory tree with actual repo state
- Corrected Vault status to Shamir unseal / file storage backend
- Moved ArgoCD, Linkerd, Grafana, Falco to roadmap section in README
- Revised microservices section to reflect one planned service (stagegrid-tickets)
- Removed stub READMEs referencing tools not yet in this repo

### Fixed
- meridian-core: removed undeclared dependencies from pyproject.toml

---

## [0.2.0] — 2026-03

### Added
- CI: container build pipeline with Cosign keyless signing (PR #2)
- CI: Dependabot configuration for GitHub Actions updates (PR #3)
- README: Current Status section with running vs roadmap breakdown

### Fixed
- Ruff lint errors (E501, I001) in meridian-core
- CI: skip ruff when no Python files present; suppress Node.js 20 deprecation warning

### Removed
- `.gitkeep`-only directories and comment-only YAML stubs
- Duplicate GCP config files (already in `observability/`)

---

## [0.1.0] — 2026-02

### Added
- On-prem stack via docker-compose: Vault, VictoriaMetrics, Quickwit, Vector, Fluent Bit, Nginx, MongoDB
- Vault: initialized and unsealed (Shamir, file storage backend); TLS throughout
- VictoriaMetrics: deployed, ingesting metrics via Node Exporter
- Quickwit: deployed for log indexing
- Vector / Fluent Bit: log collection pipeline configured end-to-end
- Nginx: TLS reverse proxy
- meridian-core: core Python library — config, Vault client, service discovery
- Observability configs: VictoriaMetrics scrape config, Quickwit index config, OTel pipeline
- Helm chart scaffold for future GitOps deployment
- AWS Vault config (planned security plane)
- STRUCTURE.md: full directory reference
- README: Meridian Software / StageGrid architecture overview
- CI: ruff linting for tools/, YAML validation for all manifests
