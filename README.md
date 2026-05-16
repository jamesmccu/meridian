# MERIDIAN LABS

MERIDIAN LABS is a modular enterprise security infrastructure simulation
platform. It models a compact distributed enterprise with branch offices, an HQ
control plane, cloud service dependencies, identity and access boundaries,
telemetry, detection engineering, and incident-response workflows.

The repository name remains `MERIDIAN`. The active project identity is MERIDIAN
LABS.

This repository is public. Do not commit private keys, certificates, tokens,
Terraform state, kubeconfigs, Vault tokens, homelab IP inventories, provider
account identifiers, or real customer data.

## Platform Intent

MERIDIAN LABS is not a certification-prep repository. Certification topics can
map indirectly to platform scenarios, but the primary unit of design is reusable
security infrastructure:

- enterprise substrate and service topology
- network segmentation and threat prevention
- Kubernetes and container platform operations
- cloud security baselines
- identity and access controls
- telemetry and observability
- detection engineering
- incident-response scenarios

The platform is intentionally local-first while it is being built. Docker
Compose, lightweight containers, structured configuration, Python tooling, and
CI checks are acceptable foundations when they make a security control testable.
Cloud, Kubernetes, and identity providers should be introduced only through
clear module contracts and validation evidence.

## Scenario

A growing company has multiple small offices connected to HQ and selected cloud
services. The initial model is compact:

```text
Branch Office A
  employee subnet
  guest subnet
  local service
  secure path to HQ

Branch Office B
  employee subnet
  guest subnet
  local service
  secure path to HQ

HQ / Control Plane
  admin workstation
  identity and access placeholder
  internal app
  telemetry collector

Cloud / External Services
  public app placeholder
  monitoring placeholder
```

The first implementation work should prove one branch and one HQ path before
duplicating the pattern.

## Current Status

MERIDIAN LABS is in an initial platform-scaffold stage. Several implementation
assets are retained from earlier MERIDIAN iterations, but not every platform
domain is implemented yet.

Implemented or retained:

- Trivy CI scanning for filesystem, image, and configuration checks.
- Python lint, type check, and test workflow for `meridian-detect`.
- Quickwit, Vector, Fluent Bit, and VictoriaMetrics configuration.
- Docker Compose reference services under `onprem/`.
- `tools/meridian-detect`, a Python CLI scaffold for future telemetry,
  enrichment, validation, and reporting workflows.
- A working vertical slice that validates the segmentation flow contract,
  validates a sample denied guest-access event, matches it to a detection rule,
  and produces a report artifact.
- Architecture, threat-model, roadmap, design-decision, and guided lab notes.

Initial scaffolds:

- `core-platform/` defines early platform topology, service, network, and
  validation contracts.
- `network-security/` introduces segmentation and connectivity as platform
  domains.
- `container-platform/`, `cloud-security/`, `identity-access/`,
  `detection-engineering/`, and `incident-response/` define target module
  boundaries.
- `observability/schemas/` introduces a first event schema contract.

## Module Map

| Current Area | Current Role | Target Platform Domain |
|---|---|---|
| `core-platform/` | Initial scaffold for shared topology, services, networks, and validation. | Core enterprise substrate. |
| `network-security/` | Initial scaffold plus structured segmentation flow contract. | Network segmentation, secure connectivity, and threat prevention. |
| `container-platform/` | Initial scaffold only. | Kubernetes and container platform operations. |
| `cloud-security/` | Initial scaffold only. | AWS/cloud security baselines and cloud control validation. |
| `identity-access/` | Initial scaffold only. | Users, roles, service identities, access policies, and audit events. |
| `observability/` | Retained Quickwit, Vector, Fluent Bit, and VictoriaMetrics configs plus schema scaffold. | Telemetry collection, routing, storage, and event schema contracts. |
| `detection-engineering/` | Initial detections, sample-events, and reports scaffold. | Detection content, test events, validation, enrichment, and reporting. |
| `incident-response/` | Initial runbook and scenario scaffold. | Investigation scenarios, response procedures, timelines, and lessons learned. |
| `tools/meridian-detect/` | Existing Python CLI scaffold with tests and packaging. | Detection engineering tooling. |
| `onprem/` | Existing Compose/Vault/Nginx reference implementation. | Candidate local substrate for `core-platform/`; preserved in place for now. |
| `security/` | Trivy configuration and security scope notes. | Repository hygiene and future policy-as-code input. |
| `labs/` | Legacy/current guided-lab content and design notes. | Migration source material for architecture-driven modules. |
| `.github/workflows/` | Existing CI and scan workflows. | Platform validation and supply-chain hygiene. |

## Existing Paths Preserved

The current implementation directories remain intact during the platform
reframe:

- `observability/`
- `onprem/`
- `tools/`
- `labs/`
- `security/`
- `scripts/`
- `.github/`

`labs/` is retained as legacy/current guided-lab content. It is not the long-term
platform architecture source of truth. New architecture-driven contracts should
land in the platform domains first, with compatibility notes added before any
future moves.

## Run The Current Checks

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

Current CLI scaffold:

```bash
make cli-help
meridian-detect --help
meridian-detect config
python3 -m meridian_detect --help
```

The `validate`, `enrich`, and `report` subcommands are placeholders for future
telemetry and detection workflows. They intentionally return a non-zero exit code
until real logic exists.

Current local Trivy checks, if Trivy is installed:

```bash
make trivy-fs
make trivy-config
```

## Near-Term Platform Work

1. Prove the first local enterprise topology contract.
2. Convert segmentation intent into validation evidence.
3. Route one safe local event through a documented telemetry schema.
4. Implement one detection/report workflow in `meridian-detect`.
5. Add identity, container, cloud, and incident-response modules only when their
   contracts and validation paths are clear.

## Intentionally Out Of Scope

MERIDIAN LABS is not trying to be:

- a production enterprise network
- a full cloud-provider reference architecture
- a compliance assurance claim
- an offensive security toolkit
- a generic observability platform
- a certification-prep repository

Any detection or traffic simulation must be local and safe. Any scanning must be
limited to lab-owned local containers or virtual machines.

## License

MIT
