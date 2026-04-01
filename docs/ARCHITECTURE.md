# Architecture

## Overview

Meridian is a multi-cloud observability and security platform built for a fictional AI hardware manufacturer. Each cloud provider is used for its genuine strengths — not duplicated for redundancy.

This document covers both the intended architecture and the current implementation state. Where they differ, both are noted explicitly.

---

## Placement Decisions

Every service lives where it does for a specific reason. The rationale should be articulable in one sentence per plane.

| Concern | AWS | GCP | Azure | On-Prem |
|---|---|---|---|---|
| Secrets management | ✅ Vault + KMS (planned) | — | — | ✅ Vault (current) |
| Runtime security | ✅ Planned (Falco, OPA) | — | — | — |
| Threat detection | ✅ Planned (GuardDuty) | — | — | — |
| Metrics storage | — | ✅ Planned (VictoriaMetrics) | — | ✅ Current |
| Log indexing | — | ✅ Planned (Quickwit) | — | ✅ Current |
| Dashboarding | — | ✅ Planned (Grafana) | — | — |
| Identity federation | — | — | ✅ Planned (Entra ID) | — |
| GitOps control | — | — | ✅ Planned (ArgoCD) | — |
| Service mesh | — | — | ✅ Planned (Linkerd) | — |
| Dev / Edge | — | — | — | ✅ Primary |
| Distributed tracing | — | — | — | ✅ Planned (Jaeger) |

---

## Current State

The full observability stack is running on a single EC2 t3.micro via docker-compose.
This is an interim configuration — the intended architecture distributes these services
across cloud planes as described below. The stack is real and operational; the placement
is being phased in.

### Running on EC2 (docker-compose)

| Service | Purpose | Status |
|---|---|---|
| Vault | Secrets management | ✅ Running, initialized, unsealed |
| VictoriaMetrics | Metrics storage | ✅ Running, scraping 3 targets |
| Quickwit | Log indexing | ✅ Running, 2 indexes created |
| Fluent Bit | Log collection | ✅ Running, reading systemd journal |
| Vector | Log shipping | ✅ Running, pipeline end-to-end verified |
| Nginx | TLS reverse proxy | ✅ Running |
| Node Exporter | Host metrics | ✅ Running |
| MongoDB | Document store | ✅ Running |

All services run TLS. Internal communication uses a self-signed root CA with
wildcard cert covering `*.meridian.local`.

---

## Intended Architecture

### AWS — Security Plane

AWS owns secrets, runtime security, and threat detection.

**Why AWS:** KMS is best-in-class for key management. GuardDuty has no real
equivalent depth in GCP or Azure. IAM gives precise, auditable control over
every API call.

Intended components:
- **Vault** with KMS auto-unseal and IAM auth backend — zero static credentials
- **Falco** with eBPF for runtime threat detection
- **OPA/Gatekeeper** policy enforcement across all clusters
- **Trivy** container scanning in CI
- **GuardDuty** findings routed via EventBridge to `alert-router`
- **ECR** container registry

Infrastructure target: k3s on EC2 t3.micro (stopped when idle, ~$0–8/mo).
Production equivalent: EKS managed node group.

**The key story:** Vault uses KMS auto-unseal so no human ever touches an unseal
key. The unseal key lives in KMS, IAM controls access, and Vault comes back up
on its own after a restart.

### GCP — Observability Plane

GCP owns metrics, logs, and dashboards.

**Why GCP:** The e2-micro is permanently free in us-central1 — not a 12-month
trial. More importantly, keeping observability in a separate cloud means monitoring
survives an AWS or Azure outage. If your monitoring goes down when AWS goes down,
your monitoring is coupled to the thing it's supposed to monitor.

Intended components:
- **VictoriaMetrics** long-term metrics storage (lower memory than Prometheus,
  compatible query language, better retention without Thanos complexity)
- **Quickwit** log indexing and search (sub-second search, minimal RAM, Grafana
  datasource plugin available)
- **Grafana** single pane of glass federating data from all providers
- **Fluent Bit / Vector** log shipping from all clusters
- **OpenTelemetry Collector** trace aggregation

Infrastructure target: e2-micro in us-central1-a (permanently free).
Production equivalent: GKE Autopilot.

### Azure — Identity & GitOps Plane

Azure owns identity federation and the GitOps control plane.

**Why Azure:** Entra ID is what enterprise shops run. Building Workload Identity
Federation on Entra ID is a skill that transfers directly to enterprise SRE roles.
ArgoCD in Azure is the only deployment path — no manual `kubectl apply` anywhere.

Intended components:
- **Entra ID** Workload Identity Federation via OIDC — no long-lived credentials
- **ArgoCD** managing deployments across all three clusters (App of Apps pattern)
- **Linkerd** service mesh with mTLS between all services
- **SOC2/PCI-DSS** compliance control mapping

Infrastructure target: k3s on B1s VM (free for 12 months).
Production equivalent: AKS.

### On-Premises — Edge / Dev Plane

On-prem simulates a constrained environment without cloud-native primitives —
no IAM, no managed load balancers, no cloud DNS. This is what edge deployments
and many on-prem Kubernetes clusters actually look like.

Current: docker-compose stack on EC2 (interim, will migrate to OrbStack on Mac).
Intended: OrbStack running k3s on MacBook Pro.

Components:
- **k3s** lightweight Kubernetes
- **Jaeger** distributed tracing UI
- **OpenTelemetry Collector** local aggregation before shipping to GCP
- **canary-analyzer** cross-cloud canary deployment and analysis

---

## Security Architecture

### Zero Credential Goal

The target security posture: no long-lived credentials anywhere in the system.

```
Developer / CI
      │
      ▼
   ArgoCD (Azure)          ← OIDC to all clusters
      │
      ├── AWS k3s           ← EC2 instance role only (no access keys)
      │     └── Vault       ← KMS auto-unseal, IAM auth
      │
      ├── GCP e2-micro      ← Workload Identity (no service account keys)
      │
      └── Azure B1s         ← Entra ID Workload Identity Federation
```

Current state: Vault is running with file storage and Shamir unseal (requires
manual unseal after restart). KMS auto-unseal is planned for the AWS plane phase.

### TLS

All internal services run TLS using a self-signed root CA. The cert covers
`*.meridian.local` with SANs for all internal service names. No service
communicates in plaintext, even within the compose network.

### Policy Enforcement (Planned)

OPA/Gatekeeper will enforce across all clusters:
- No containers running as root
- No privileged pods
- Required resource limits
- Approved registries only
- Required labels on all workloads

---

## Observability Architecture

### Current Data Flow

```
EC2 host (systemd journal)
      │
      ▼
  Fluent Bit              ← reads journal, tails /var/log/*.log
      │ (forward/TLS)
      ▼
  Vector                  ← normalizes and batches
      │ (HTTPS via nginx)
      ▼
  Quickwit                ← indexes logs (otel-logs-v0_7)

  Node Exporter
      │
      ▼
  VictoriaMetrics         ← scrapes every 15s, stores metrics
```

### Intended Data Flow (Multi-Cloud)

```
All clusters (AWS, GCP, Azure, On-prem)
      │
      ▼
  Fluent Bit / Vector     ← log shipping from all nodes
      │
      ▼
  Quickwit (GCP)          ← centralized log indexing

  py-exporter (all nodes)
      │
      ▼
  VictoriaMetrics (GCP)   ← long-term metrics storage
      │
      ▼
  Grafana (GCP)           ← unified dashboards

  OTel Collector (all nodes)
      │
      ▼
  Jaeger (On-prem)        ← trace storage and UI
```

---

## GitOps Architecture (Planned)

ArgoCD will run in Azure as the only deployment path.

```
Git (main branch)
      │
      ▼
   ArgoCD (Azure)
      │
      ├── App: aws-security-plane     → AWS k3s
      ├── App: gcp-observability      → GCP e2-micro
      ├── App: azure-identity         → Azure B1s
      └── App: onprem-edge            → OrbStack k3s
```

No one applies manifests manually. All cluster credentials stored in Vault,
fetched by ArgoCD at sync time.

---

## Cost Architecture

### Lab vs Production

| Component | Lab | Production equivalent |
|---|---|---|
| AWS compute | t3.micro (docker-compose now, k3s later) | EKS managed node group |
| GCP compute | e2-micro k3s | GKE Autopilot |
| Azure compute | B1s k3s | AKS |
| Secrets | Vault OSS, file storage | Vault Enterprise, Raft + KMS unseal |
| Service mesh | Linkerd | Linkerd or Istio |

### Target Monthly Cost

| Component | Cost |
|---|---|
| GCP e2-micro | Free (permanent) |
| Azure B1s | Free (12 months) |
| AWS t3.micro (stopped when idle) | ~$0–8/mo |
| OrbStack | Free |
| **Total** | **< $10/mo** |

k3s on single VMs instead of managed Kubernetes reduces cost by ~95% while
preserving all architectural decisions. This is documented as a lab constraint,
not an architectural preference.

---

## Compliance Mapping (Planned)

| Control area | Mechanism |
|---|---|
| Access control | Vault + OIDC, no shared credentials |
| Audit logging | All API calls logged to Quickwit |
| Change management | ArgoCD is the only deploy path, all changes in Git |
| Vulnerability management | Trivy in CI, Falco runtime detection |
| Incident response | alert-router → PagerDuty, runbooks in OPERATIONS.md |
| Encryption in transit | Linkerd mTLS + TLS on all current services |
| Encryption at rest | KMS-backed Vault (planned), cloud provider disk encryption |
