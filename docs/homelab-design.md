# Homelab Design

Meridian is intentionally homelab-first. The homelab is the primary learning and
execution environment for the platform, not a reduced copy of a cloud deployment.

## Rationale

The target skill set includes Linux internals, Kubernetes, system design,
distributed systems, observability, security tooling, and GitOps/IaC. Those areas
are best learned when the operator owns the failure modes.

Running the platform locally makes the following visible:

- Host networking, DNS, ports, TLS, firewall behavior, and packet flow.
- Process lifecycle, systemd units, journald, audit logs, and file permissions.
- Container runtime behavior, cgroups, resource limits, and storage pressure.
- Kubernetes scheduling, service discovery, ingress, secrets, and network policy.
- Telemetry collection, buffering, parsing, storage, retention, and alerting.
- Backup and recovery for services that do not have managed cloud safety nets.

## Recommended Homelab Runtime Path

Meridian should evolve in stages:

| Stage | Runtime | Purpose |
|---|---|---|
| 1 | Docker Compose | Keep a simple local baseline for Vault, telemetry, proxying, and data services. |
| 2 | Single-node k3s | Learn Kubernetes packaging, ingress, secrets, storage, and GitOps reconciliation. |
| 3 | Multi-node k3s | Learn scheduling, node failure, persistent storage, service disruption, and network policy. |
| 4 | Hardened platform | Add runtime detection, admission control, backup workflows, and incident runbooks. |

## Recommended Core Components

| Component | Recommendation | Why |
|---|---|---|
| Kubernetes | k3s | Lightweight, realistic, widely used in labs and edge environments. |
| CNI | Cilium | Teaches Kubernetes networking, eBPF visibility, and network policy. |
| GitOps | Argo CD | Clear reconciliation model and strong visual demonstration value. |
| Ingress | ingress-nginx or Traefik | Standard HTTP entry point for hosted services. |
| Certificates | cert-manager | Automates certificate lifecycle and teaches cluster-level trust automation. |
| Secrets | Vault plus External Secrets or Vault Secrets Operator | Preserves explicit secrets management while integrating with Kubernetes. |
| Metrics | VictoriaMetrics | Efficient Prometheus-compatible metrics backend for constrained hardware. |
| Logs | Quickwit or Loki | Local log search without requiring a SaaS dependency. |
| Traces | Tempo or Jaeger | Distributed tracing for representative services. |
| Collection | OpenTelemetry Collector | Common telemetry pipeline that can export locally and to Datadog. |
| Runtime security | Falco | Kernel/runtime detection with practical security signals. |
| Policy | OPA/Gatekeeper or Kyverno | Admission control and policy-as-code practice. |

## Homelab Boundary

The homelab should own:

- Platform runtime.
- Internal observability.
- Local secrets and PKI experiments.
- Kubernetes policy and runtime security controls.
- Representative hosted services.
- Backup/restore drills.
- Failure injection and recovery practice.

The homelab should not pretend to be:

- A fully managed cloud provider.
- A certified compliance environment.
- A replacement for cloud IAM, cloud KMS, public DNS, or managed threat detection.

## Operating Principles

- Prefer simple working systems before adding abstractions.
- Every component should have a reason tied to the learning goals.
- Every public-facing service should have documented ingress, TLS, logging, and
  rollback behavior.
- Every security tool should produce evidence, not just exist in the stack.
- Every cloud dependency should have a clear reason and cost boundary.
