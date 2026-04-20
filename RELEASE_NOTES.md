# Release Notes — Meridian Platform

Milestone summaries for the Meridian SRE Platform. For a full change history see [CHANGELOG.md](./CHANGELOG.md).

---

## v0.3.0 — Docs & Reconciliation (April 2026)

Focus: architecture documentation brought into sync with actual state.

- README and STRUCTURE.md now accurately reflect what is running vs. what is planned
- Vault status corrected to Shamir unseal / file storage (not KMS — that's a roadmap item)
- Removed placeholder stubs for tools and services not yet implemented
- meridian-core dependency declarations cleaned up

**Status after this release:** on-prem stack running, CI green, docs accurate.

---

## v0.2.0 — CI Pipeline (March 2026)

Focus: supply chain security and automated dependency management.

- Container image builds signed via **Cosign keyless signing** on every push to main
- **Dependabot** configured for GitHub Actions updates
- Ruff linting enforced in CI for all Python in `tools/`
- YAML manifest validation runs on every PR

**Status after this release:** every push produces a signed container; lint and validation gates prevent broken manifests from merging.

---

## v0.1.0 — On-Prem Foundation (February 2026)

Focus: working observability and security stack running locally via docker-compose.

**Running:**
- **Vault** — secrets management, PKI, short-lived credentials; Shamir unseal, file storage
- **VictoriaMetrics** — metrics ingestion via Node Exporter scrape
- **Quickwit** — log indexing and search
- **Vector + Fluent Bit** — log collection and shipping pipeline
- **Nginx** — TLS reverse proxy for all services
- **MongoDB** — document store
- **meridian-core** — shared Python library: config, Vault client, service discovery

**Architecture established:**
- Multi-cloud placement design: AWS (security), GCP (observability), Azure (identity/GitOps), on-prem (foundation)
- SLO targets defined for all four StageGrid services
- PCI-DSS and SOC2 compliance design targets documented

This release represents the working baseline from which all cloud planes will be built.

---

## Roadmap

| Milestone | Target |
|---|---|
| v0.4.0 — GCP Observability Plane | VictoriaMetrics + Quickwit + Grafana on e2-micro |
| v0.5.0 — stagegrid-tickets | First StageGrid service (FastAPI, OpenTelemetry, Redis) |
| v0.6.0 — AWS Security Plane | Vault KMS auto-unseal, Falco, OPA/Gatekeeper |
| v0.7.0 — GitOps | ArgoCD App of Apps, Linkerd mTLS |
| v1.0.0 — Full Multi-Cloud | All four planes running, all five StageGrid services deployed |
