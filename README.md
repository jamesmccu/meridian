# Meridian Software — SRE Platform

A portfolio-grade SRE platform built to production standards. Meridian Software's primary product is **StageGrid** — a live events ticketing platform — running across a multi-cloud, multi-cluster Kubernetes environment with full observability, security, and identity management.

> Built by [James McCulley](https://jamesmcculley.dev) — Senior SRE  
> GitHub: [github.com/jamesmcculley](https://github.com/jamesmcculley)

---

## Why This Project Exists

Most portfolio infrastructure projects deploy a generic app and call it done. This one is different. Meridian is built to answer a specific question: *what does a senior SRE's platform actually look like when it's designed for real operational complexity?*

StageGrid's traffic profile — sharp on-sale spikes, high checkout criticality, async notification fanout — forces real decisions about autoscaling, SLO design, failure domain isolation, and chaos engineering. Every tool in this stack earned its place.

---

## Architecture Overview

**Meridian Software** is the fictional company. **StageGrid** is the product — a live events ticketing and infrastructure platform. The Meridian Platform is the SRE layer that runs it.

### Infrastructure

| Cluster | Provider | Runtime | Role |
|---|---|---|---|
| meridian-onprem | On-premises (MacBook Pro) | k3s / OrbStack | FreeIPA, Vault, dev workloads |
| meridian-aws | AWS | EKS | Primary StageGrid production workloads |
| meridian-azure | Azure | AKS | Secondary region, DR, chaos targets |

Clusters are connected via **Tailscale** mesh VPN. **Linkerd** provides mTLS and traffic observability within each cluster.

### StageGrid Services

StageGrid's service architecture covers five bounded domains. The first service to be implemented is `stagegrid-tickets` — a Python/FastAPI application handling seat reservation and checkout, instrumented with OpenTelemetry for distributed tracing. The remaining four services are planned and will follow.

| Service | Responsibility | SLO target | Status |
|---|---|---|---|
| stagegrid-tickets | Seat reservation and checkout | 99.9% | Building next |
| stagegrid-catalog | Event and venue browse | 99.5% | Planned |
| stagegrid-notify | Fan notification fanout | 99.0% | Planned |
| stagegrid-identity | Auth and access control | 99.9% | Planned |
| stagegrid-loadgen | Synthetic traffic generation | — | Planned |

### Observability Stack

| Pillar | Tool |
|---|---|
| Metrics | VictoriaMetrics |
| Logs | Quickwit |
| Traces | Jaeger |
| Collection | Fluent Bit + Vector |
| Instrumentation | OpenTelemetry |

### Security Stack

- **Falco** (eBPF) — runtime syscall monitoring and anomaly detection
- **OPA / Gatekeeper** — Kubernetes admission control policies
- **Trivy** — container image vulnerability scanning in the ArgoCD pipeline
- **HashiCorp Vault** — secrets management, PKI, short-lived credentials
- **Linkerd mTLS** — encrypted, authenticated service-to-service communication

### Identity & Access Management

A layered identity model separating end-user, operator, and platform identity planes:

| Layer | Provider | Scope |
|---|---|---|
| End users | Okta OIDC | StageGrid fan authentication |
| Operators | Okta OIDC / SAML | Internal admin portal |
| Unix / infrastructure | FreeIPA | SSH, sudo, host enrollment, LDAP |
| Secrets | HashiCorp Vault | Service credentials, PKI, TLS |

FreeIPA provides centralized Unix identity management for all on-premises infrastructure — host enrollment, SSH key management, sudo policy via HBAC rules, and LDAP directory services. This is the on-prem analog to enterprise PAM platforms (Delinea Server Suite, Centrify AD Bridging).

### GitOps & Deployment

**ArgoCD** manages all cluster state. Every manifest, Helm values file, and OPA policy is version-controlled in this repository. No manual kubectl applies in production.

---

## Python Tooling

All platform tooling is written in Python, built without AI assistance, and lives in `/tools`.

| Tool | Description |
|---|---|
| `meridian-core` | Shared library: config, logging, Vault client, service discovery |
| `logparse` | Log parsing and structured event extraction from Quickwit |
| `py-exporter` | Custom VictoriaMetrics exporter for StageGrid business metrics |
| `alert-router` | Alert routing and enrichment; integrates with VictoriaMetrics alertmanager |
| `atlas-ops` | Operational automation: node drain, certificate rotation, chaos experiments |
| `canary-analyzer` | Automated canary analysis using VictoriaMetrics metrics |

---

## Repository Structure

```
/
├── README.md
├── OPERATIONS.md          # Internal — operational runbooks and procedures
├── TROUBLESHOOTING.md     # Internal — break/fix patterns and known issues
├── platform/              # Shared infrastructure: ArgoCD, Vault, Linkerd, Tailscale
├── clusters/              # Per-cluster Helm values and kustomize overlays
│   ├── onprem/
│   ├── aws/
│   └── azure/
├── services/              # StageGrid microservices
│   ├── stagegrid-tickets/
│   ├── stagegrid-catalog/
│   ├── stagegrid-notify/
│   ├── stagegrid-identity/
│   └── stagegrid-loadgen/
├── identity/              # FreeIPA manifests, Ansible host enrollment, Okta config
├── observability/         # VictoriaMetrics, Quickwit, Jaeger, Fluent Bit, Vector
├── security/              # Falco rules, OPA policies, Trivy pipeline config
└── tools/                 # Python tooling ecosystem
```

---

## SLO Design

SLOs are defined for each StageGrid service and tracked in VictoriaMetrics. Burn rate alerting fires at 1-hour and 6-hour windows.

| Service | Target | 30-Day Error Budget |
|---|---|---|
| stagegrid-tickets | 99.9% availability | 43.2 minutes |
| stagegrid-catalog | 99.5% availability | 3.6 hours |
| stagegrid-notify | 99.0% availability | 7.2 hours |
| stagegrid-identity | 99.9% availability | 43.2 minutes |

---

## Compliance

- **PCI-DSS** — stagegrid-tickets is PCI-scoped. Vault manages credentials with short-lived leases and full audit logging. Network policies isolate PCI workloads to dedicated namespaces.
- **SOC2 Type II** — Access control, audit logging, and change management controls mapped across the platform.

---

## Contact

**James McCulley** — Senior Site Reliability Engineer  
[jamesmcculley.dev](https://jamesmcculley.dev) · [github.com/jamesmcculley](https://github.com/jamesmcculley)



## Current Status

> Last updated: April 2026

### Running

All services below run via docker-compose in the `onprem/` configuration with TLS throughout.

- **Vault** — initialized and unsealed (Shamir unseal, file storage backend); KMS auto-unseal planned
- **VictoriaMetrics** — deployed, ingesting metrics via Node Exporter
- **Quickwit** — deployed for log indexing
- **Vector / Fluent Bit** — log collection and shipping pipeline configured end-to-end
- **Nginx** — TLS reverse proxy
- **MongoDB** — running via docker-compose

### Roadmap

The following are planned but not yet deployed:

- **GCP observability plane** — migrate VictoriaMetrics, Quickwit, and Grafana to a GCP e2-micro (permanently free tier); next active work item
- **Falco** — eBPF runtime security monitoring
- **OPA/Gatekeeper** — Kubernetes admission control policies
- **ArgoCD** — GitOps control plane, App of Apps pattern
- **Linkerd** — service mesh with mTLS across all services
- **KMS auto-unseal** — Vault auto-unseal via AWS KMS, eliminating manual operator unseal

### Intended Architecture

The table below describes the target multi-cloud placement. It is an architecture target, not a description of current state.

| Plane | Cloud | Intended components |
|---|---|---|
| Security | AWS | Vault (KMS auto-unseal), Falco, GuardDuty, OPA |
| Observability | GCP | VictoriaMetrics, Quickwit, Grafana |
| Identity / GitOps | Azure | Entra ID, ArgoCD, Linkerd |
| Edge / dev | On-prem | docker-compose stack (current), k3s (planned) |
