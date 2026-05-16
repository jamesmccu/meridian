# Repository Structure

MERIDIAN LABS is being reframed into a modular enterprise security
infrastructure simulation platform. Existing implementation directories are
preserved while new architecture-driven module scaffolds are introduced.

```text
MERIDIAN/
├── .github/
│   └── workflows/
│       ├── build-sign.yml          # meridian-detect image build/sign workflow
│       ├── lint.yml                # Python lint, type checks, and tests
│       ├── trivy-scan.yml          # Trivy filesystem, image, and config scans
│       └── validate-manifests.yml  # YAML validation
├── core-platform/                  # Initial enterprise substrate contracts
│   ├── topology/                   # Local enterprise topology contract
│   ├── services/                   # Service catalog contract
│   ├── networks/                   # Network and zone catalog contract
│   └── validation/                 # Shared validation expectations
├── network-security/               # Segmentation and connectivity modules
│   ├── segmentation/
│   │   └── flows.yaml              # Structured segmentation flow contract
│   └── connectivity/
├── container-platform/             # Planned container/Kubernetes operations domain
├── cloud-security/                 # Planned cloud security baseline domain
├── identity-access/                # Planned identity and access domain
├── detection-engineering/          # Detection content and sample-event scaffolds
│   ├── detections/
│   ├── reports/
│   └── sample-events/
├── incident-response/              # Runbook and scenario scaffolds
│   ├── runbooks/
│   └── scenarios/
├── docs/
│   ├── architecture.md             # Distributed enterprise model
│   ├── design-decisions.md         # Repo audit and pivot decisions
│   ├── interview-positioning.md    # Development note, not source of truth
│   ├── learning-map.md             # Development note, not source of truth
│   ├── roadmap.md                  # Phased planning context
│   ├── threat-model.md             # Initial threat model
│   └── runbooks/
│       └── README.md               # Legacy/planned operational runbook notes
├── diagrams/
│   └── README.md                   # Placeholder for reviewed lab diagrams
├── labs/                           # Legacy/current guided-lab content
│   ├── 01-network-segmentation-trust-boundaries/
│   ├── 02-secure-connectivity-remote-access/
│   ├── 03-host-hardening-baseline-enforcement/
│   ├── 04-telemetry-detection-response/
│   ├── 05-policy-as-code-automated-validation/
│   └── README.md
├── observability/                  # Retained telemetry configs and schema scaffold
│   ├── schemas/
│   ├── quickwit/
│   ├── otel/
│   └── victoriametrics/
├── onprem/                         # Existing Compose/Vault/Nginx reference material
├── security/                       # Security tooling docs and Trivy config
├── scripts/                        # Existing helper scripts
├── tools/
│   └── meridian-detect/            # Current Python detection CLI scaffold
├── README.md
├── SECURITY.md
├── RELEASE_NOTES.md
├── STRUCTURE.md
└── CHANGELOG.md
```

## Active Platform Domains

- `core-platform/`: initial contracts for topology, services, networks, and
  validation.
- `network-security/`: segmentation and connectivity contracts.
- `observability/`: retained telemetry pipeline configuration and event schemas.
- `detection-engineering/`: sample events, detection scaffolds, and report
  scaffolds.
- `incident-response/`: initial scenario and runbook scaffolds.

## Planned Platform Domains

- `container-platform/`: Kubernetes and container platform operations.
- `cloud-security/`: cloud security baselines and policy validation.
- `identity-access/`: users, roles, service identities, access policy, and audit
  events.

## Preserved Compatibility Areas

The following existing directories are intentionally left in place during this
phase:

- `observability/`
- `onprem/`
- `tools/`
- `labs/`
- `security/`
- `scripts/`
- `.github/`

`labs/` remains legacy/current guided-lab content and migration source material.
It is not the long-term platform architecture source of truth.
