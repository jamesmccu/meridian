# Changelog

All notable changes to the Meridian Platform are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

### Added
- Homelab-first architecture documentation under `docs/`
- ADR 0001 documenting the homelab-first platform decision
- Cloud boundary guidance for AWS, optional GCP, and Datadog usage
- Learning map tying Meridian work to Python DSA, Linux internals, Kubernetes,
  distributed systems, observability, security tooling, and GitOps/IaC
- Static site migration plan for hosting a public site on Meridian
- Runbook directory with planned operational runbooks
- GitOps directory placeholders for hosted applications and platform components
- Infrastructure directory placeholders for Ansible and OpenTofu
- Public security policy
- `meridian-core` command-line diagnostic entry point

### Changed
- Reframed Meridian as a platform for hosted services rather than a named
  application workload
- Updated repository structure documentation to include docs and current workflows
- Expanded `.gitignore` coverage for local tool state, secrets, kubeconfigs,
  Terraform/OpenTofu state, and generated runtime data
- Corrected on-prem Compose mounts to reference observability configuration files
  in their actual repository locations
- Quoted Prometheus scrape targets so YAML validation parses consistently
- Tightened documentation language to distinguish configured, planned, and
  implemented functionality
- Improved `meridian-core` test ergonomics and type annotations
- Expanded the Python quality workflow to run Ruff, mypy, and pytest
- Fixed YAML validation workflow dependency installation
- Updated GitHub Actions versions for Node 24 compatibility
- Made PR image scanning informational while keeping filesystem scanning as the
  hard Trivy vulnerability gate

### Planned
- Observability foundation — dashboards, traces, alerting, and optional Datadog export
- Falco eBPF runtime security monitoring
- OPA/Gatekeeper Kubernetes admission control
- ArgoCD GitOps control plane (App of Apps pattern)
- Linkerd service mesh with mTLS
- KMS auto-unseal for Vault
- First representative hosted service for exercising platform controls

---

## [0.3.0] — 2026-04

### Changed
- Reconciled STRUCTURE.md and README directory tree with actual repo state
- Corrected Vault status to Shamir unseal / file storage backend
- Moved ArgoCD, Linkerd, Grafana, Falco to roadmap section in README
- Revised hosted services section to reflect current platform scope
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
- CI: skip ruff when no Python files present; suppress then-current Node.js deprecation warning

### Removed
- `.gitkeep`-only directories and comment-only YAML stubs
- Duplicate GCP config files (already in `observability/`)

---

## [0.1.0] — 2026-02

### Added
- On-prem stack via docker-compose: Vault, VictoriaMetrics, Quickwit, Vector, Fluent Bit, Nginx, MongoDB
- Vault configuration using Shamir unseal and file storage
- VictoriaMetrics scrape configuration
- Quickwit log indexing configuration
- Vector / Fluent Bit log collection pipeline configuration
- Nginx TLS reverse proxy configuration
- meridian-core: core Python library for shared platform configuration
- Observability configs: VictoriaMetrics scrape config, Quickwit index config, OTel pipeline
- Helm chart scaffold for future GitOps deployment
- AWS Vault config (planned security plane)
- STRUCTURE.md: full directory reference
- README: Meridian platform architecture overview
- CI: ruff linting for tools/, YAML validation for all manifests
