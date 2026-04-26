# ADR 0001: Homelab-First Platform

## Status

Accepted

## Context

Meridian is intended to build and demonstrate competence across Python tooling,
Linux internals, Kubernetes, system design, distributed systems, observability,
security tooling, and GitOps/IaC.

A fully managed cloud-first design would make some parts easier to deploy, but it
would also hide many of the lower-level systems this project is meant to expose:
host operations, container runtime behavior, networking, storage, telemetry
pipelines, and failure recovery.

At the same time, a purely on-premises design would miss important cloud-native
security concepts such as IAM, KMS, public DNS, managed threat detection, and
durable object storage.

## Decision

Meridian will be homelab-first.

The primary runtime target is owned infrastructure. Cloud services will be added
selectively when they teach provider-native capabilities that cannot be represented
honestly in the homelab.

## Consequences

Positive:

- The project exposes Linux, Kubernetes, networking, storage, TLS, and observability
  details directly.
- Cost stays manageable.
- Failure modes are visible and can be practiced.
- The platform can host real services without requiring every service to depend on
  a public cloud provider.
- Cloud usage becomes easier to justify because each dependency has a specific
  learning or operational purpose.

Negative:

- The homelab requires more operational work than managed cloud services.
- Availability depends on residential power, internet, and hardware unless cloud
  failover is later added.
- Some production-grade capabilities will need to be documented as limitations.
- Public exposure requires careful DNS, ingress, TLS, and security controls.

## Implementation Guidance

- Keep Docker Compose as a simple baseline until Kubernetes replaces specific
  services.
- Move toward k3s for the main platform runtime.
- Use GitOps for Kubernetes state.
- Use Ansible for homelab host bootstrap.
- Use OpenTofu/Terraform for cloud resources.
- Use AWS first for IAM, KMS, DNS, backup storage, and managed security findings.
- Add GCP only when it has a clear purpose.
- Keep local observability primary and treat Datadog as an optional integration,
  not the only source of telemetry.
