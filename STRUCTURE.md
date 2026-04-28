# Repository Structure

```text
MERIDIAN/
├── .github/
│   └── workflows/
│       ├── build-sign.yml          # meridian-core image build/sign workflow
│       ├── lint.yml                # Python lint, type checks, and tests
│       ├── trivy-scan.yml          # Trivy filesystem, image, and config scans
│       └── validate-manifests.yml  # YAML validation
├── docs/
│   ├── architecture.md             # Active MERIDIAN v2 architecture
│   ├── learning-map.md             # Detection engineering learning map
│   └── runbooks/
│       └── README.md               # Planned operational runbooks
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
│   └── meridian-core/              # Current Python diagnostics package
├── README.md
├── SECURITY.md
├── RELEASE_NOTES.md
├── STRUCTURE.md
└── CHANGELOG.md
```

## Active Scope

MERIDIAN v2 is focused on Kubernetes runtime detection engineering.

Active areas:

- detection architecture documentation
- security scanning CI
- Quickwit and event-routing configuration
- Python diagnostics package

Planned active areas:

- Falco rules
- detection catalog
- sample events
- synthetic detection tests
- Python enrichment and reporting
- Kubernetes deployment profiles

## Archived Scope

Earlier platform-era concepts were archived in the
`meridian-v1-platform-archive` Git tag. They are not part of the default branch
because they do not support the v2 detection engineering scope.
