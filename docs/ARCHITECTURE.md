# Architecture

## Overview

Meridian is a multi-cloud observability and security platform built for a fictional AI hardware manufacturer. It is designed to demonstrate intentional cloud placement — each provider is used for its genuine strengths, not as a redundancy exercise.

This document reflects the intended architecture. See the Status table in the README for what is currently running.

---

## Placement Decisions

### Why not the same stack in every cloud?

Copying identical tooling across three clouds demonstrates cost, not architecture. The goal is to show that a senior SRE thinks about *why* a workload lives where it does.

### Decision Matrix

| Concern | AWS | GCP | Azure | On-Prem |
|---|---|---|---|---|
| Secrets management | ✅ Primary (KMS + Vault) | — | — | — |
| Runtime security | ✅ Primary (Falco, OPA) | — | — | — |
| Threat detection | ✅ Primary (GuardDuty) | — | — | — |
| Metrics storage | — | ✅ Primary (VictoriaMetrics) | — | — |
| Log indexing | — | ✅ Primary (Quickwit) | — | — |
| Dashboarding | — | ✅ Primary (Grafana) | — | — |
| Identity federation | — | — | ✅ Primary (Entra ID) | — |
| GitOps control | — | — | ✅ Primary (ArgoCD) | — |
| Service mesh | — | — | ✅ Primary (Linkerd) | — |
| Local dev / edge | — | — | — | ✅ Primary |
| Distributed tracing | Collector | Collector | Collector | ✅ UI (Jaeger) |

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
      ├── AWS k3s           ← EC2 instance role (no keys)
      │     └── Vault       ← KMS auto-unseal, IAM auth
      │
      ├── GCP e2-micro      ← Workload Identity (no key files)
      │
      └── Azure B1s         ← Entra ID Workload Identity Federation
```

**Vault** is the intended secrets authority. All dynamic credentials (DB passwords, API tokens, TLS certs) will be issued by Vault with short TTLs and automatic rotation.

**KMS auto-unseal** means Vault never requires a human to unseal after a restart. The unseal key lives in AWS KMS, access controlled by IAM.

**OIDC/Workload Identity** will be used everywhere instead of service account keys or static IAM credentials.

### Policy Enforcement (Planned)

OPA/Gatekeeper will run on all clusters enforcing:
- No containers running as root
- No privileged pods
- Required resource limits on all containers
- Approved container registries only
- Required labels on all workloads

### Runtime Detection (Planned)

Falco will run on AWS with eBPF (no kernel module required). Alerts will flow to `alert-router`, which normalizes them alongside GuardDuty findings and routes to the appropriate channel.

---

## Observability Architecture

### Intended Data Flow

```
All clusters (AWS, GCP, Azure, On-prem)
      │
      ▼
  Fluent Bit / Vector          ← log shipping
      │
      ▼
  Quickwit (GCP)               ← log indexing + search

  OTel Collector (all nodes)
      │
      ▼
  Jaeger (On-prem)             ← trace storage + UI

  py-exporter (all nodes)
      │
      ▼
  VictoriaMetrics (GCP)        ← long-term metrics storage
      │
      ▼
  Grafana (GCP)                ← unified dashboards
```

### Why VictoriaMetrics over Prometheus?

- Significantly lower memory footprint — important on free-tier GCP
- Compatible with Prometheus query language and scrape configs
- Better long-term retention without Thanos complexity
- Remote write compatible — any Prometheus instance can ship to it

### Why Quickwit over Elasticsearch/Loki?

- Sub-second search on large datasets with minimal RAM
- Designed for cloud-native object storage backends
- Grafana datasource plugin available
- Cost-appropriate for a lab budget

---

## GitOps Architecture (Planned)

ArgoCD will run in Azure as the only deployment path. No one applies manifests manually.

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

---

## Cost Architecture

### Lab vs Production

| Component | Lab | Production equivalent |
|---|---|---|
| AWS compute | t3.micro k3s | EKS managed node group |
| GCP compute | e2-micro k3s | GKE Autopilot |
| Azure compute | B1s k3s | AKS |
| Secrets | Vault OSS | Vault Enterprise or HCP Vault |
| Service mesh | Linkerd | Linkerd or Istio |

### Spin-up/Spin-down Strategy

AWS and Azure nodes are stopped when not actively being developed. GCP e2-micro runs continuously (free). On-prem runs continuously via OrbStack at no cost.

### Target Monthly Cost

| Component | Cost |
|---|---|
| GCP e2-micro | Free (permanent) |
| Azure B1s | Free (12 months) |
| AWS t3.micro (stopped when idle) | ~$0–8/mo |
| OrbStack | Free |
| **Total** | **< $10/mo** |

---

## Compliance Mapping (Planned)

SOC2 Trust Service Criteria and PCI-DSS controls will be mapped to platform components in `compliance/`.

| Control area | Mechanism |
|---|---|
| Access control | Vault + OIDC, no shared credentials |
| Audit logging | All API calls logged to Quickwit |
| Change management | ArgoCD is the only deploy path, all changes in Git |
| Vulnerability management | Trivy scanning in CI, Falco runtime detection |
| Incident response | alert-router → PagerDuty, runbooks in OPERATIONS.md |
| Encryption in transit | Linkerd mTLS between all services |
| Encryption at rest | KMS-backed Vault, cloud provider disk encryption |
