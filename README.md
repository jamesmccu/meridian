# MERIDIAN LABS

Hands-on distributed office security lab for modeling how small branch offices
connect securely to a main office and cloud services.

MERIDIAN LABS keeps the repository name `MERIDIAN` and pivots the project from a
Kubernetes runtime detection-only lab into a broader security architecture lab.
The retained v2 detection and telemetry work becomes one module in the new lab
rather than the entire project.

This repository is public. Do not commit private keys, certificates, tokens,
Terraform state, kubeconfigs, Vault tokens, homelab IP inventories, provider
account identifiers, or real customer data.

## Why This Exists

Many security engineering roles require practical judgment across network
segmentation, secure connectivity, endpoint and host controls, telemetry,
detection, and automation. MERIDIAN LABS is designed to make those decisions
visible in a small but realistic environment.

The goal is not to simulate an enterprise at full scale. The goal is to build a
clear, reviewable lab that demonstrates how a growing company can secure small
offices that depend on HQ services and cloud applications.

## Scenario

A growing company has multiple small offices connected to HQ and cloud services.
The initial model is intentionally compact:

```text
Branch Office A
  employee subnet
  guest subnet
  local service
  secure tunnel to HQ

Branch Office B
  employee subnet
  guest subnet
  local service
  secure tunnel to HQ

HQ / Main Office
  admin workstation
  identity-like service placeholder
  internal app
  logging / telemetry collector

Cloud
  public app placeholder
  monitoring placeholder
```

## Security Problems Demonstrated

MERIDIAN LABS is organized around practical controls:

- network segmentation between employee, guest, service, HQ, and cloud zones
- secure branch-to-HQ connectivity
- baseline host hardening and configuration management
- telemetry collection, detection logic, and local reporting
- policy-as-code and CI checks for configuration hygiene
- architecture documentation and threat modeling

Existing MERIDIAN v2 telemetry assets are preserved as future input for
`labs/04-telemetry-detection/`.

## Senior Engineering Signal

The lab maps to real senior security engineering work by showing:

- architecture tradeoffs and trust boundaries before tool selection
- control-plane versus branch-office responsibilities
- local-first implementation choices that can later map to enterprise tooling
- automation boundaries that avoid hiding important learning work
- detection and incident-readiness thinking tied to network design
- CI/CD hygiene for security configuration without making CI the product

## Current Status

MERIDIAN LABS is in the repositioning and scaffold stage.

Implemented or retained:

- Trivy CI scanning for filesystem, image, and configuration checks.
- Python lint, type check, and test workflow for `meridian-detect`.
- Quickwit, Vector, Fluent Bit, and VictoriaMetrics configuration from v2.
- Docker Compose lab services from earlier iterations.
- `tools/meridian-detect`, a small Python CLI scaffold for future telemetry,
  enrichment, and reporting workflows.
- Documentation for the distributed office architecture, threat model, roadmap,
  design decisions, and interview positioning.

Planned next:

- lab-owned topology and segmentation examples
- secure branch connectivity exercise
- host hardening exercise
- local telemetry/detection exercise built from the retained v2 assets
- policy-as-code and CI validation exercise
- incident-response scenarios after the first controls exist

## Repository Structure

```text
MERIDIAN/
├── docs/                     # Architecture, threat model, roadmap, decisions
├── labs/                     # Hands-on lab modules and learning tasks
├── observability/            # Retained v2 event pipeline configuration
├── onprem/                   # Retained Compose/Vault/Nginx reference material
├── security/                 # Security tooling docs and Trivy config
├── tools/meridian-detect/    # Retained Python telemetry/detection scaffold
├── README.md
├── SECURITY.md
└── STRUCTURE.md
```

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

## Roadmap

- Phase 1: topology and segmentation
- Phase 2: VPN / secure connectivity
- Phase 3: host hardening
- Phase 4: telemetry and detection
- Phase 5: policy-as-code / CI checks
- Phase 6: incident-response scenarios

See [docs/roadmap.md](docs/roadmap.md) for the detailed phased plan.

## Intentionally Out Of Scope

MERIDIAN LABS is not trying to be:

- a full restaurant-specific proof of concept
- a production enterprise network
- an offensive security toolkit
- a cloud-provider-specific reference architecture
- a compliance certification claim
- a service mesh, GitOps platform, or generic observability platform

Any detection or traffic simulation must be local and safe. Any scanning must be
limited to lab-owned local containers or virtual machines.

## License

MIT
