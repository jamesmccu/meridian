# Repository Structure

```text
MERIDIAN/
├── .github/
│   └── workflows/
│       ├── build-sign.yml          # meridian-detect image build/sign workflow
│       ├── lint.yml                # Python lint, type checks, and tests
│       ├── trivy-scan.yml          # Trivy filesystem, image, and config scans
│       └── validate-manifests.yml  # YAML validation
├── docs/
│   ├── architecture.md             # MERIDIAN LABS distributed office model
│   ├── design-decisions.md         # Repo audit and pivot decisions
│   ├── interview-positioning.md    # Senior-role discussion guide
│   ├── learning-map.md             # Retained v2 learning map
│   ├── roadmap.md                  # Phased lab roadmap
│   ├── threat-model.md             # Initial threat model
│   └── runbooks/
│       └── README.md               # Planned operational runbooks
├── diagrams/
│   └── README.md                   # Placeholder for reviewed lab diagrams
├── labs/
│   ├── 01-network-segmentation-trust-boundaries/
│   ├── 02-secure-connectivity-remote-access/
│   ├── 03-host-hardening-baseline-enforcement/
│   ├── 04-telemetry-detection-response/
│   ├── 05-policy-as-code-automated-validation/
│   └── README.md
├── observability/
│   ├── quickwit/
│   │   └── quickwit.yaml           # Searchable event backend config
│   ├── otel/
│   │   ├── fluent-bit.conf         # Legacy log forwarding config
│   │   └── vector.yaml             # Event/log routing config
│   └── victoriametrics/
│       └── prometheus.yml          # Legacy metrics scrape config
├── onprem/
│   ├── docker-compose.yml          # Legacy Compose lab
│   ├── nginx/nginx.conf            # Legacy TLS reverse proxy config
│   ├── node-exporter/web.yml       # Legacy Node Exporter TLS config
│   └── vault/config/vault.hcl      # Legacy Vault config
├── security/
│   ├── README.md                   # Active security scope
│   └── trivy/
│       ├── README.md
│       └── trivy.yaml
├── tools/
│   └── meridian-detect/            # Current Python CLI scaffold
├── README.md
├── SECURITY.md
├── RELEASE_NOTES.md
├── STRUCTURE.md
└── CHANGELOG.md
```

## Active Scope

MERIDIAN LABS is focused on distributed office security architecture and
implementation practice.

Active areas:

- architecture and threat-model documentation
- branch, HQ, and cloud lab design
- security scanning CI
- retained Quickwit and event-routing configuration
- retained Python CLI scaffold for telemetry/detection workflow commands

Planned active areas:

- network segmentation and trust-boundaries lab
- secure connectivity and remote-access lab
- host hardening and baseline-enforcement lab
- telemetry, detection, and response lab
- policy-as-code and automated-validation lab
- incident-response scenarios

## Archived Scope

Earlier platform-era concepts were archived in the
`meridian-v1-platform-archive` Git tag. They are not part of the default branch
because they do not support the MERIDIAN LABS scope.
