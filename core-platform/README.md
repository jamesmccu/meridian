# Core Platform

`core-platform/` is the initial scaffold for MERIDIAN LABS shared enterprise
substrate. It defines platform contracts that other modules can depend on:
topology, services, network zones, and validation expectations.

This directory is not a replacement for the existing `onprem/` implementation
yet. The current Compose-based reference stack remains in `onprem/` until a
future migration can preserve compatibility and validation behavior.

## Current Scope

- Define the local enterprise topology contract.
- Define service and network catalogs for early modules.
- Document validation expectations before implementation expands.
- Provide a stable place for reusable substrate design.

## Planned Scope

- Local Compose or lightweight VM substrate.
- Shared certificate and naming conventions.
- Common health checks and evidence capture.
- Compatibility mapping from existing `onprem/` services.

## Not Implemented Yet

- A complete enterprise runtime.
- Kubernetes cluster provisioning.
- Cloud account provisioning.
- Production-grade identity or network enforcement.
