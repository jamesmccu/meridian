# Repository Structure

```
meridian/
├── .github/
│   └── workflows/
│       ├── build-sign.yml          # Container build + Cosign keyless signing
│       ├── lint.yml                 # Python lint, type checks, and tests
│       ├── trivy-scan.yml          # Trivy filesystem, image, and config scans
│       └── validate-manifests.yml  # YAML validation for all manifests
├── aws/
│   └── vault/
│       └── config/vault.hcl        # Vault server config for AWS plane (planned)
├── docs/
│   ├── adr/
│   │   └── 0001-homelab-first-platform.md
│   ├── runbooks/
│   │   └── README.md
│   ├── architecture.md             # Platform architecture and target direction
│   ├── cloud-boundaries.md         # Why/when cloud belongs in Meridian
│   ├── homelab-design.md           # Homelab-first design rationale
│   ├── learning-map.md             # Skill goals mapped to platform work
│   └── static-site-migration.md    # Plan for hosting a static site on Meridian
├── onprem/
│   ├── docker-compose.yml          # On-prem stack: Vault, VictoriaMetrics, Quickwit, Nginx, MongoDB
│   ├── nginx/nginx.conf            # TLS reverse proxy config
│   ├── node-exporter/web.yml       # Node Exporter TLS config
│   └── vault/config/vault.hcl     # Vault server config for on-prem
├── observability/
│   ├── victoriametrics/
│   │   └── prometheus.yml          # VictoriaMetrics scrape config
│   ├── quickwit/
│   │   └── quickwit.yaml           # Quickwit index and ingest config
│   └── otel/
│       ├── fluent-bit.conf         # Fluent Bit log forwarding config
│       └── vector.yaml             # Vector pipeline config
├── security/
│   └── README.md                   # Security tooling overview
├── gitops/
│   ├── apps/
│   │   └── README.md               # Future hosted application desired state
│   ├── helm/
│   │   └── meridian-chart/
│   │       ├── Chart.yaml
│   │       └── values.yaml
│   ├── platform/
│   │   └── README.md               # Future platform component desired state
│   └── README.md
├── infra/
│   ├── ansible/
│   │   └── README.md               # Future homelab host bootstrap
│   ├── opentofu/
│   │   ├── aws/
│   │   │   └── README.md           # Future AWS cloud primitives
│   │   ├── gcp/
│   │   │   └── README.md           # Optional future GCP experiments
│   │   └── README.md
│   └── README.md
├── tools/
│   └── meridian-core/              # Core Python library for platform configuration
│       └── src/meridian_core/__main__.py
├── README.md                       # Project overview
├── SECURITY.md                     # Public security policy
├── MIGRATION_STATUS.md             # Multi-repo migration status
├── RELEASE_NOTES.md                # Milestone summaries
├── STRUCTURE.md                    # This file
└── CHANGELOG.md                    # Change history
```

## Environments

| Directory | Environment | Runtime | Status |
|---|---|---|---|
| `onprem/` | On-premises | docker-compose | Active — current foundation |
| `gitops/` | Homelab Kubernetes | Helm / future GitOps | Scaffolded |
| `infra/ansible/` | Homelab hosts | Ansible | Planned |
| `infra/opentofu/aws/` | AWS | OpenTofu | Planned |
| `infra/opentofu/gcp/` | GCP | OpenTofu | Optional future path |
| `aws/` | AWS | Provider-native services / future k3s experiments | Planned — cloud security and platform primitives |
