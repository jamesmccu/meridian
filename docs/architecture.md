# Meridian Architecture

Meridian is a homelab-first platform for running services with production-style
security, observability, and delivery practices. It is not an application. It is
the platform layer that applications can run on.

## Design Goals

- Build practical competence in Linux, Kubernetes, security tooling, observability,
  distributed systems, GitOps, and infrastructure as code.
- Keep the core platform runnable on owned hardware so the underlying systems are
  visible and debuggable.
- Use cloud services selectively when they teach capabilities that are hard to
  reproduce honestly on-premises.
- Keep implementation status explicit so planned architecture is not confused
  with deployed functionality.
- Make design choices explainable to engineers reviewing the project.

## Current State

The current repository contains a Docker Compose based platform foundation:

- Vault for local secrets management configuration.
- VictoriaMetrics and Node Exporter configuration for metrics.
- Quickwit, Fluent Bit, and Vector configuration for logs.
- Nginx TLS reverse proxy configuration.
- MongoDB as a local data service.
- Trivy, Cosign, Ruff, and YAML validation workflows in CI.
- `meridian-core`, a small Python support package.
- A Helm chart scaffold for future Kubernetes/GitOps deployment.

This foundation is useful because it lets the platform start with real services,
TLS configuration, telemetry components, and CI gates before introducing the
additional operational complexity of Kubernetes.

## Target State

The target platform is Kubernetes-first while remaining homelab-first.

```text
Developer Git Push
        |
        v
GitHub Actions
  - lint
  - tests
  - manifest validation
  - Trivy scans
  - image signing
        |
        v
GitOps Repository State
        |
        v
Argo CD / Flux
        |
        v
Homelab Kubernetes
  - ingress
  - cert management
  - secrets integration
  - network policy
  - observability agents
  - hosted services
        |
        v
Telemetry and Security Backends
  - metrics
  - logs
  - traces
  - runtime detections
```

## Platform Planes

| Plane | Primary Location | Purpose |
|---|---|---|
| Runtime | Homelab Kubernetes | Run platform services and hosted applications. |
| Observability | Homelab first, optional Datadog export | Collect metrics, logs, and traces locally; selectively forward SaaS telemetry when useful. |
| Security | Homelab plus selective cloud | Combine local controls with cloud-native security services. |
| Delivery | GitHub Actions and GitOps | Build, scan, sign, and reconcile platform state. |
| Cloud integration | AWS first, GCP optional | Use cloud primitives where they teach IAM, KMS, DNS, object storage, and managed detection. |

## Why Homelab First

Running Meridian on owned infrastructure forces direct interaction with the
substrate that managed services hide:

- Linux processes, filesystems, networking, cgroups, systemd, and kernel telemetry.
- Kubernetes control plane behavior, scheduling, ingress, service discovery,
  storage, and network policy.
- TLS certificate lifecycle, reverse proxy behavior, and local trust roots.
- Observability pipeline failures and storage tradeoffs.
- Backup, restore, resource pressure, and node failure scenarios.

The homelab is not only a cheaper deployment target. It is part of the learning
model.

## Why Use Cloud At All

Some platform capabilities are cloud-native and should be learned in the cloud:

- IAM and workload identity.
- KMS-backed encryption workflows.
- Durable object storage for backups.
- Public DNS and edge exposure.
- Managed threat detection such as GuardDuty.
- Cloud posture and account-level security findings.
- Multi-cloud trust boundaries and connectivity patterns.

Cloud usage should stay selective. If a capability can be learned better by
running it directly in the homelab, it belongs on-premises. If the point is to
learn a cloud-native control plane or security primitive, it belongs in cloud.

## Recommended Stack Direction

| Domain | Recommended Meridian Implementation |
|---|---|
| Python DSA | Platform CLIs, parsers, alert enrichment, SLO calculators, inventory tools. |
| Linux internals | Node hardening, auditd, eBPF experiments, journald/log forwarding, cgroup visibility. |
| Kubernetes | k3s, Helm, ingress, cert-manager, Cilium, NetworkPolicies, operators. |
| System design | Architecture docs, ADRs, threat model, runbooks, failure-mode documentation. |
| Distributed systems | Small representative services for retries, queues, idempotency, tracing, and failure injection. |
| Observability | VictoriaMetrics, Quickwit or Loki, Grafana, OpenTelemetry Collector, optional Datadog export. |
| Security tooling | Vault, Trivy, Cosign, Falco, OPA/Gatekeeper or Kyverno, auditd, osquery. |
| GitOps/IaC | Argo CD or Flux, Helm, Ansible for homelab bootstrap, OpenTofu/Terraform for cloud. |
| Multi-cloud | AWS first for IAM/KMS/DNS/security services; GCP only where it has a specific learning purpose. |
| Datadog | Optional agent/APM integration with strict telemetry filtering and cost controls. |

## Hosted Services

Hosted services should be treated as consumers of Meridian. A service is a good
candidate for the platform when it can exercise one or more platform concerns:

- TLS ingress.
- CI build, scan, and signing.
- GitOps deployment.
- Runtime health checks.
- Metrics, logs, and traces.
- Secrets access.
- Backup and restore.
- Security policy enforcement.

A static portfolio or documentation site is a strong first candidate because it
is real, low risk, public-facing, and easy to evaluate before moving more complex
services.
