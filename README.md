# Meridian

**Security-focused observability platform for a realistic cloud operations environment.**

Meridian is a portfolio infrastructure project that shows how security engineering,
network security, and SRE practices fit together around an enterprise-style platform.
The repository currently contains the on-premises foundation, CI/security scanning
configuration, observability configuration, Vault configuration, and a small Python
support library. The broader homelab and selective-cloud architecture is documented
as the target direction and is being migrated into a split-repository layout.

Built by [James McCulley](https://jamesmcculley.dev)

GitHub: [github.com/jamesmcculley](https://github.com/jamesmcculley)

---

## Executive Summary

Meridian models the platform foundation for services that need secure runtime
infrastructure, strong telemetry, and clear operational controls. It is intended
to provide the environment that application services can live on, not to be an
application itself.

The current repository demonstrates:

- A local/on-premises platform stack using Docker Compose.
- Secrets management with HashiCorp Vault using TLS, Shamir unseal, and file
  storage for the current lab environment.
- Metrics and log collection components built around VictoriaMetrics, Quickwit,
  Fluent Bit, and Vector.
- Nginx as a TLS reverse proxy for local services.
- MongoDB as a local data service for future hosted services.
- CI checks for Python linting, type checks, tests, YAML validation, Trivy
  scanning, and Cosign keyless image signing for `meridian-core` when its image
  workflow runs.
- A small Python package, `meridian-core`, for shared platform configuration.

This repository is not a production deployment. It is an engineering artifact that
shows platform design, security control selection, operational tradeoffs, and the
current implementation state of a larger security/SRE lab.

This is a public repository. Do not commit private keys, certificates, tokens,
Terraform state, kubeconfigs, Vault tokens, homelab IP inventories, or provider
account identifiers. Generated local certs and runtime data are intentionally
ignored.

The design is homelab-first by intent. Running the platform on owned infrastructure
keeps Linux, Kubernetes, networking, storage, TLS, and telemetry behavior visible.
Cloud services are added selectively where they teach cloud-native security and
platform concepts such as IAM, KMS, public DNS, durable object storage, and managed
threat detection.

---

## Problem Statement

Security engineering projects often show individual tools in isolation: a scanner,
a SIEM component, a Kubernetes policy, or an infrastructure module. Real platform
work is more integrated. Secrets, network boundaries, telemetry, CI gates, runtime
controls, and operational procedures need to support each other.

Meridian is built to answer a practical question:

> How would a small platform team design a cost-conscious environment that still
> demonstrates credible security, observability, and operational discipline?

The project focuses on:

- Creating a working foundation before adding cloud complexity.
- Making security controls observable and testable.
- Separating implemented functionality from planned architecture.
- Keeping the system small enough to run as a lab while preserving realistic
  enterprise design concerns.

The design rationale is documented in:

- [Architecture](./docs/architecture.md)
- [Homelab Design](./docs/homelab-design.md)
- [Cloud Boundaries](./docs/cloud-boundaries.md)
- [Learning Map](./docs/learning-map.md)
- [ADR 0001: Homelab-First Platform](./docs/adr/0001-homelab-first-platform.md)

---

## Architecture

### Current Implementation

The current implementation is centered on a local/on-premises stack and supporting
repository automation.

| Area | Components | Status |
|---|---|---|
| Secrets | Vault with TLS, Shamir unseal, file storage | Implemented in config |
| Metrics | VictoriaMetrics, Node Exporter scrape config | Configured |
| Logs | Fluent Bit, Vector, Quickwit | Configured |
| Reverse proxy | Nginx with TLS configuration | Configured |
| Data service | MongoDB with TLS options in Compose | Configured |
| Python tooling | `meridian-core` package | Implemented |
| CI | Ruff lint, mypy, pytest, YAML validation, Trivy scans, Cosign signing | Configured |
| GitOps | Helm chart scaffold | Placeholder |

Key directories:

```text
meridian/
├── .github/workflows/          # CI, validation, image signing, security scans
├── aws/vault/                  # Planned AWS Vault configuration
├── docs/                       # Architecture, design rationale, ADRs, runbooks
├── gitops/                     # Helm scaffold and future GitOps desired state
├── infra/                      # Future Ansible and OpenTofu infrastructure code
├── observability/              # Metrics, log, and collector configuration
├── onprem/                     # Local Docker Compose stack and service configs
├── security/trivy/             # Trivy scan configuration and documentation
├── tools/meridian-core/        # Python support library
├── MIGRATION_STATUS.md         # Multi-repo migration tracker
├── STRUCTURE.md                # Repository structure reference
└── CHANGELOG.md                # Change history
```

### Target Architecture

The intended architecture uses the local stack as the foundation for a staged
platform with selective cloud integrations:

| Plane | Intended Role | Current State |
|---|---|---|
| On-prem/local | Lab foundation for Vault, metrics, logs, proxy, data service | Present in this repo |
| AWS | Security and secrets plane, including future KMS-backed Vault and native threat detection | Planned |
| GCP | Optional comparison path for workload identity, storage, observability, or external observer experiments | Optional future path |
| GitOps/Kubernetes | Declarative deployment, policy enforcement, service mesh | Scaffolded/planned |

The target design includes additional controls such as GuardDuty, Security Hub,
OPA/Gatekeeper, Falco, Linkerd, network policies, and cloud flow log analysis.
Those controls are roadmap items unless explicitly represented by files in this
repository or linked split repositories.

### Repository Split

Meridian is being transitioned from a single repository into a corporate-style
multi-repo layout:

- [meridian-platform](https://github.com/jamesmcculley/meridian-platform) -
  infrastructure, GitOps, observability, and shared platform tooling.
- [meridian-api](https://github.com/jamesmcculley/meridian-api) - backend services
  and API contracts.
- [meridian-web](https://github.com/jamesmcculley/meridian-web) - frontend and
  dashboard applications.
- [meridian-security](https://github.com/jamesmcculley/meridian-security) -
  security controls, policies, and detection engineering.
- [meridian-docs](https://github.com/jamesmcculley/meridian-docs) - architecture
  docs, ADRs, runbooks, and release notes.

During the migration, this repository remains the umbrella view and status tracker.
See [MIGRATION_STATUS.md](./MIGRATION_STATUS.md) for the current migration map.

A static portfolio or documentation site is being considered as the first real
hosted service on Meridian. The migration plan is documented in
[Static Site Migration](./docs/static-site-migration.md). The site source should
remain in its own repository; Meridian should provide the runtime, ingress, TLS,
deployment, and observability foundation.

---

## Security Relevance

Meridian is designed to demonstrate security engineering decisions across the
platform lifecycle.

### Implemented or Configured

- **Secrets management:** Vault configuration is present for the local stack,
  using TLS and file storage in the current lab environment.
- **Transport security:** Nginx, Vault, VictoriaMetrics, Node Exporter, and MongoDB
  configurations reference TLS certificates.
- **Vulnerability scanning:** Trivy filesystem, image, and config scans are defined
  in GitHub Actions. Filesystem and image scans fail on `CRITICAL` and `HIGH`
  findings.
- **Supply chain security:** `meridian-core` container images are built and signed
  with Cosign keyless signing on `main` pushes that touch the package or image
  workflow.
- **Manifest validation:** YAML validation runs in CI with PyYAML.
- **Python quality checks:** Ruff, mypy, and pytest run against Python code under
  `tools/`.
- **Risk tracking:** The Trivy ignore list is intentionally empty until a finding
  is reviewed and accepted.

### Planned

- AWS KMS auto-unseal for Vault.
- AWS GuardDuty and Security Hub.
- OPA/Gatekeeper admission policies.
- Falco runtime detection.
- Kubernetes NetworkPolicies and Calico.
- Linkerd service mesh mTLS.
- Cloud WAF controls.
- Flow log collection and network anomaly analysis.
- Compliance dashboards and stronger evidence mapping.

### Compliance Orientation

The project is oriented around controls commonly associated with NIST 800-53,
PCI-DSS, and SOC 2, but the current repository should be read as a lab and design
artifact rather than a certified compliance implementation. Current compliance
value comes from the control mapping, CI/security automation, TLS-first service
configuration, and explicit separation of implemented controls from roadmap items.

---

## Usage

### Prerequisites

Expected local tools:

- Docker with Compose support.
- Python 3.12 for `meridian-core`.
- `pip` or another Python package installer.
- Optional: Trivy and Cosign for reproducing CI security checks locally.

The on-premises Compose configuration expects local TLS certificate files under
`onprem/certs/`. Certificates are not committed to the repository.

### Run Python Tests

From the repository root:

```bash
cd tools/meridian-core
python3 -m pip install -e ".[dev]"
python3 -m pytest
```

### Run Python Linting

```bash
cd tools/meridian-core
python3 -m ruff check .
```

### Validate YAML Manifests

The CI workflow validates YAML files with Python and PyYAML. Locally, use an
equivalent YAML validation command or run the workflow in GitHub Actions.

### Run Security Scans Locally

If Trivy is installed:

```bash
trivy fs --config security/trivy/trivy.yaml .
trivy config --config security/trivy/trivy.yaml .
```

The image scan in CI targets:

```text
ghcr.io/jamesmcculley/meridian-core:latest
```

### Start the Local Stack

The local stack is defined in [onprem/docker-compose.yml](./onprem/docker-compose.yml).
Before starting it, provide the expected TLS certificates under `onprem/certs/`
and verify that the mounted configuration paths match the files in your checkout.

```bash
cd onprem
docker compose up -d
```

Useful follow-up checks:

```bash
docker compose ps
docker compose logs vault
docker compose logs victoriametrics
docker compose logs quickwit
```

The Compose stack is the local foundation for the project. Cloud deployment,
GitOps deployment, hosted application services, and Kubernetes security controls
are not fully implemented in this repository yet.

---

## Roadmap

Near-term work is focused on making the current foundation easier to verify and
then moving selected components into the split repositories.

| Milestone | Scope | Status |
|---|---|---|
| Documentation reconciliation | Keep README, STRUCTURE, release notes, and migration status aligned with the repo | In progress |
| Local stack hardening | Document cert generation, service health checks, and recovery steps | Planned |
| CI baseline | Keep linting, type checks, tests, YAML validation, Trivy scans, and image signing stable | Configured |
| Security evidence | Add clearer mapping from controls to files, workflows, and verification commands | Planned |
| Static site migration | Move a static site from managed static hosting to Meridian as the first hosted service | Planned |
| GitOps foundation | Expand the Helm scaffold into deployable platform manifests | Planned |
| IaC foundation | Add Ansible homelab bootstrap and OpenTofu cloud modules | Planned |
| Runtime controls | Add OPA/Gatekeeper, Falco, and network policy examples | Planned |
| Cloud security plane | Move toward AWS-backed Vault, KMS auto-unseal, GuardDuty, and Security Hub | Planned |
| Observability foundation | Add dashboards, traces, alerting, and optional Datadog export | Planned |
| Hosted services | Add representative services that exercise SLOs, audit logging, identity, and security controls | Planned |

See [CHANGELOG.md](./CHANGELOG.md) and [RELEASE_NOTES.md](./RELEASE_NOTES.md) for
release history.

---

## License

MIT
