# Release Notes — Meridian Platform

Milestone summaries for the Meridian SRE Platform. For a full change history see [CHANGELOG.md](./CHANGELOG.md).

## Unreleased — Homelab Platform Direction

Focus: clarify Meridian as a homelab-first platform that can host services.

- Added architecture, homelab design, cloud boundary, and learning map docs
- Added ADR 0001 for the homelab-first platform decision
- Added a migration plan for hosting a static site on Meridian
- Added GitOps and infrastructure placeholders for hosted applications, platform
  components, Ansible, and OpenTofu
- Added a public security policy and broader ignore rules for local/private state
- Corrected on-prem Compose mounts for observability config files
- Expanded Python CI to run linting, type checks, and tests
- Fixed YAML validation workflow dependency installation
- Tightened wording around configured versus implemented functionality
- Reframed hosted services as consumers of the platform rather than the purpose of
  the platform itself
- Updated structure documentation to reflect the new docs and current workflows

**Status after this update:** the design rationale is documented; Kubernetes,
GitOps, and static-site hosting remain planned implementation work.

---

## v0.3.0 — Docs & Reconciliation (April 2026)

Focus: architecture documentation brought into sync with actual state.

- README and STRUCTURE.md now accurately reflect what is running vs. what is planned
- Vault status corrected to Shamir unseal / file storage (not KMS — that's a roadmap item)
- Removed placeholder stubs for tools and services not yet implemented
- meridian-core dependency declarations cleaned up

**Status after this release:** on-prem configuration present, CI configured, docs
reconciled with repository state.

---

## v0.2.0 — CI Pipeline (March 2026)

Focus: supply chain security and automated dependency management.

- `meridian-core` container image builds signed via **Cosign keyless signing** on
  matching pushes to main
- **Dependabot** configured for GitHub Actions updates
- Ruff linting enforced in CI for all Python in `tools/`
- YAML manifest validation runs on every PR

**Status after this release:** pushes that touch `meridian-core` produce a signed
container image; lint and validation gates prevent broken manifests from merging.

---

## v0.1.0 — On-Prem Foundation (February 2026)

Focus: observability and security stack foundation configured for local
docker-compose use.

**Configured in this repository:**
- **Vault** — secrets management configuration using Shamir unseal and file storage
- **VictoriaMetrics** — metrics scrape configuration
- **Quickwit** — log indexing configuration
- **Vector + Fluent Bit** — log collection pipeline configuration
- **Nginx** — TLS reverse proxy configuration
- **MongoDB** — document store service in Compose
- **meridian-core** — shared Python library for platform configuration

**Architecture established:**
- Multi-cloud placement design: AWS for security primitives, optional GCP for future comparison, on-prem as the foundation
- Initial SLO and service-hosting concepts for future representative workloads
- PCI-DSS and SOC2 compliance design targets documented

This release represents the working baseline from which the homelab platform and
selective cloud integrations will be built.

---

## Roadmap

| Milestone | Target |
|---|---|
| v0.4.0 — Homelab Kubernetes | k3s, ingress, TLS automation, and GitOps bootstrap |
| v0.5.0 — Static Site Hosting | Static site planned as the first Meridian-hosted service |
| v0.6.0 — AWS Security Plane | Vault KMS auto-unseal, GuardDuty, Security Hub, and backup storage |
| v0.7.0 — Runtime Controls | Falco, OPA/Gatekeeper or Kyverno, and network policy enforcement |
| v1.0.0 — Platform Baseline | Homelab platform running with documented cloud boundaries, observability, security controls, and hosted services |
