# MERIDIAN v2 Architecture

MERIDIAN v2 is a Kubernetes runtime detection engineering lab. The architecture
is intentionally small so the detection workflow is easy to run, inspect, and
explain.

## Scope

MERIDIAN v2 focuses on:

- runtime security detection logic
- Kubernetes event generation and validation
- searchable detection events
- Python enrichment and reporting
- MITRE ATT&CK mapping

MERIDIAN v2 does not try to be a full SRE observability platform, GitOps platform,
multi-cloud lab, or compliance implementation.

## Target Event Flow

```text
Kubernetes workload behavior
        |
        v
Falco runtime rule
        |
        v
Falco JSON event
        |
        v
Vector route / transform
        |
        v
Quickwit index
        |
        v
Python enrichment / correlation
        |
        v
Finding, report, alert payload, or metric
```

## Component Responsibilities

| Component | Responsibility | Required for v2 Core |
|---|---|---|
| Kubernetes | Provides the runtime environment where detections are exercised. | Yes |
| Falco | Detects runtime behavior from syscall/container signals. | Yes |
| Vector | Routes Falco events to the backend and optional outputs. | Yes |
| Quickwit | Stores searchable detection events. | Yes |
| Python tooling | Enriches events, maps detections, and emits reports. | Yes |
| Trivy | Scans repository/config/image artifacts in CI. | Yes |
| Metrics backend | Shows detection/test metrics. | Optional |
| Cloud provider | Supplies managed Kubernetes or future cloud event sources. | Optional |

## Platform-Agnostic Model

The core detection workflow should run on any Kubernetes environment where Falco
can run with the required permissions.

Provider-specific behavior belongs in profiles:

- `local-k3s`
- `kind`
- `eks`
- `gke`
- `aks`

The base design should not require cloud IAM, cloud logging, managed DNS, service
mesh, or GitOps tooling.

## Detection Evidence

Each detection should eventually have:

- Falco rule.
- sample raw event.
- expected enriched finding.
- MITRE ATT&CK mapping.
- synthetic trigger or test script.
- false-positive notes.
- validation status.

This evidence model is the core hiring signal for the project.
