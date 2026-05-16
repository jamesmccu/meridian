# Container Platform

`container-platform/` is the planned home for Kubernetes and container platform
operations scenarios.

This directory is an initial scaffold. No active Kubernetes cluster profile,
network policy, admission control, or runtime security implementation exists in
this module yet.

## Planned Scope

- Local cluster profile.
- Namespace and workload baseline.
- Kubernetes network policies.
- Admission or policy validation.
- Runtime telemetry and detection hooks.

## Boundary

Container platform work should support MERIDIAN LABS enterprise simulation
goals. It should not become a standalone Kubernetes study track.
