# MERIDIAN

**Kubernetes runtime detection engineering lab.**

MERIDIAN is being repositioned as a focused platform for building, testing, and
validating runtime security detections in Kubernetes environments. The project is
intended to be platform-agnostic: the core detection workflow should work on k3s,
kind, self-managed Kubernetes, EKS, GKE, AKS, or any cluster that can run the
required sensor and event pipeline.

This repository is public. Do not commit private keys, certificates, tokens,
Terraform state, kubeconfigs, Vault tokens, homelab IP inventories, or provider
account identifiers.

---

## Current Status

MERIDIAN v2 is a repositioning effort. The current repository contains useful
building blocks, but the full detection loop is not implemented yet.

Implemented or configured:

- Trivy CI scanning for filesystem, image, and config checks.
- GitHub Actions quality checks for Python, YAML, and security scanning.
- Quickwit configuration for searchable event storage.
- Vector and Fluent Bit configuration that can support event routing.
- Docker Compose lab services from the previous platform iteration.
- A small Python package, `meridian-core`, currently limited to configuration
  diagnostics.

Planned for v2:

- Falco runtime detection rules.
- A Kubernetes lab profile for local testing.
- Synthetic adversary/test scripts.
- Sample Falco events.
- MITRE ATT&CK mapping.
- Python enrichment and correlation for runtime events.
- A detection catalog with validation status.

Not active v2 scope:

- multi-cloud platform architecture
- static site hosting
- broad SRE observability platform
- Vault-backed secrets platform
- GitOps delivery platform
- service mesh
- compliance certification claims

Earlier platform-oriented material was archived in the
`meridian-v1-platform-archive` Git tag and is no longer part of the default
branch.

---

## Project Goal

Security detections should be testable. MERIDIAN v2 focuses on a small, repeatable
workflow:

1. Write a runtime detection.
2. Trigger representative behavior in Kubernetes.
3. Capture the event.
4. Enrich and normalize the event.
5. Map it to MITRE ATT&CK.
6. Validate that the expected detection fired.
7. Produce a searchable finding or report.

The goal is not to build a generic observability platform. The goal is to make
runtime detection engineering concrete and reviewable.

---

## Target Architecture

The v2 architecture should stay intentionally small:

```text
Kubernetes cluster
  |
  | runtime activity
  v
Falco
  |
  | JSON events
  v
Vector
  |
  v
Quickwit
  |
  v
Python enrichment / correlation
  |
  v
Detection report, alert payload, or metrics
```

Core components:

| Component | Role | Current State |
|---|---|---|
| Kubernetes | Runtime environment for detection testing | Planned |
| Falco | Runtime event sensor and rule engine | Planned |
| Vector | Event routing and normalization pipeline | Config present |
| Quickwit | Searchable event backend | Config present |
| Python tooling | Enrichment, correlation, reporting | Minimal config package only |
| Trivy | CI vulnerability and config scanning | Configured |

The default local target should be k3s or kind. Provider-specific profiles for
EKS, GKE, or AKS should be adapters, not required architecture.

---

## Repository Structure

```text
MERIDIAN/
├── .github/workflows/        # CI quality, validation, and security scans
├── docs/                     # Active v2 design and runbook docs
├── observability/            # Quickwit and event pipeline configuration
├── onprem/                   # Existing Compose lab from earlier iteration
├── security/                 # Security tooling docs and Trivy config
├── tools/meridian-core/      # Current Python package; planned enrichment home
├── README.md
├── SECURITY.md
└── STRUCTURE.md
```

Expected future v2 structure:

```text
detections/
  falco/
  mitre-map.yml
  tests/

events/
  samples/

deploy/
  profiles/
    local-k3s/
    eks/
    gke/
    aks/

tools/
  meridian-detect/
```

These directories should be added only when there is working content behind them.

---

## Alerting And Observability

The v2 proof of concept should produce evidence in three forms:

- searchable events in Quickwit
- enriched JSON findings from Python tooling
- detection metrics or a generated report showing rule hits and test results

Recommended alert outputs:

- local JSON report first
- webhook or Slack-style payload later
- Alertmanager or Datadog export only after the local detection loop works

Recommended metrics:

- `meridian_detection_events_total`
- `meridian_detection_events_by_rule`
- `meridian_detection_events_by_severity`
- `meridian_detection_events_by_mitre_tactic`
- `meridian_enrichment_errors_total`
- `meridian_test_cases_passed_total`
- `meridian_test_cases_failed_total`

Metrics are useful for the POC, but they should support the detection workflow
rather than become a separate observability platform.

---

## Platform-Agnostic Design

MERIDIAN should not depend on one cloud provider or one Kubernetes distribution.

Design rules:

- Keep base manifests free of provider-specific annotations.
- Put EKS, GKE, AKS, and local settings in separate profiles or overlays.
- Use Falco JSON as the primary event contract.
- Treat cloud audit logs as future inputs, not required v2 dependencies.
- Keep Quickwit as the default local backend.
- Make external alert sinks optional.

This keeps the project relevant to on-prem, managed Kubernetes, and public-sector
or enterprise environments without over-building cloud-specific features.

---

## Security Scope

Current active security tooling:

- Trivy CI scanning.
- Public security policy.
- Ignore rules for local/private state.

Planned detection scope:

- container escape indicators
- suspicious shell execution
- credential file access
- Kubernetes service account token access
- unexpected egress patterns
- crypto-mining indicators
- network tooling inside workload containers

Each detection should eventually include:

- rule ID
- description
- severity
- data source
- MITRE ATT&CK tactic and technique
- expected event fields
- false-positive notes
- synthetic test coverage
- validation status

---

## Usage

Bootstrap a local development environment:

```bash
make bootstrap
```

Current local checks:

```bash
make test
make lint
make typecheck
make yaml
make compose
make check
```

Current local Trivy checks, if Trivy is installed:

```bash
make trivy-fs
make trivy-config
```

Equivalent direct Python commands:

```bash
python3 -m pytest tools/meridian-core/tests
python3 -m ruff check tools/meridian-core
python3 -m mypy tools/meridian-core/src
```

The Compose lab is not the final MERIDIAN v2 runtime architecture.

---

## Roadmap

Near term:

- rewrite `security/README.md` around local detection ownership
- add Falco rule directory
- add sample Falco JSON events
- define detection catalog schema
- add MITRE ATT&CK mapping
- build Python event enrichment/report output

Later:

- local k3s deployment profile
- synthetic adversary test scripts
- Quickwit saved queries or documented searches
- optional metrics export
- optional provider profiles for EKS, GKE, and AKS

Out of scope until the detection loop works:

- cloud security planes
- GitOps platform delivery
- Datadog integration
- OPA/Gatekeeper enforcement
- compliance mapping

---

## License

MIT
