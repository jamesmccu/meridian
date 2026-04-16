# Repository Structure

```
meridian/
├── .github/
│   └── workflows/
│       ├── lint.yml                 # Ruff linting for tools/
│       └── validate-manifests.yml  # YAML validation for all manifests
├── aws/
│   └── vault/
│       └── config/vault.hcl        # Vault server config for AWS plane (planned)
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
│   └── helm/
│       └── meridian-chart/
│           ├── Chart.yaml
│           └── values.yaml
├── tools/
│   └── meridian-core/              # Core Python library — config, Vault client, service discovery
├── README.md                       # Project overview
├── STRUCTURE.md                    # This file
└── CHANGELOG.md                    # Change history
```

## Cloud environments

| Directory | Environment | Runtime | Status |
|---|---|---|---|
| `onprem/` | On-premises | docker-compose | Active — current foundation |
| `aws/` | AWS | k3s on EC2 t3.micro | Planned — security plane |
| `gcp/` | GCP | k3s on e2-micro | Planned — observability plane |
| `azure/` | Azure | k3s on B1s | Planned — identity / GitOps plane |
