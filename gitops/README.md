# GitOps

This directory is the future home for Kubernetes desired state.

Current state:

- `helm/meridian-chart/` contains the initial Helm chart scaffold.
- `apps/` is reserved for hosted services that consume the Meridian platform.
- `platform/` is reserved for platform components such as ingress, certificates,
  observability agents, policy controllers, and runtime security tooling.

No production-ready GitOps deployment is present yet.
