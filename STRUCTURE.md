# Repository Structure

```
meridian/
├── .github/
│   └── workflows/
│       ├── lint.yml                 # Ruff linting for tools/
│       └── validate-manifests.yml  # YAML validation for all manifests
├── aws/
│   └── vault/
│       └── config/vault.hcl        # Vault server config for AWS
├── azure/                          # Azure cluster config (Terraform — coming soon)
├── gcp/                            # GCP cluster config (Terraform — coming soon)
├── onprem/
│   ├── docker-compose.yml          # Local stack: VM, Quickwit, Vault, Nginx
│   ├── nginx/nginx.conf            # Reverse proxy config
│   ├── node-exporter/web.yml       # Node exporter TLS config
│   └── vault/config/vault.hcl     # Vault server config for on-prem
├── observability/
│   ├── victoriametrics/
│   │   └── prometheus.yml          # VictoriaMetrics scrape config
│   ├── quickwit/
│   │   └── quickwit.yaml           # Quickwit index and ingest config
│   ├── otel/
│   │   ├── fluent-bit.conf         # Fluent Bit log forwarding config
│   │   └── vector.yaml             # Vector pipeline config
│   └── jaeger/                     # Jaeger tracing config (coming soon)
├── security/
│   ├── README.md                   # Links to jamesmcculley/security-tools
│   ├── falco/README.md             # Links to jamesmcculley/security-tools
│   ├── opa/README.md               # Links to jamesmcculley/security-tools
│   └── trivy/                      # Trivy operator config (coming soon)
├── gitops/
│   ├── argocd/
│   │   └── app-of-apps.yaml        # ArgoCD app of apps bootstrap
│   └── helm/
│       └── meridian-chart/
│           ├── Chart.yaml
│           └── values.yaml
├── tools/
│   ├── meridian-core/              # Core Python library — config, clients, utilities
│   ├── alert-router/               # Alert routing and deduplication (placeholder)
│   ├── canary-analyzer/            # Canary deployment analysis (placeholder)
│   ├── logparse/                   # Log parsing utilities (placeholder)
│   ├── atlas-ops/                  # MongoDB Atlas operations (placeholder)
│   └── py-exporter/                # Custom Prometheus exporter (placeholder)
├── docs/                           # Project documentation (under review)
├── README.md                       # Project overview
├── OPERATIONS.md                   # Operational runbook
├── TROUBLESHOOTING.md              # Troubleshooting guide
└── CHANGELOG.md                    # Change history
```

## Cloud environments

| Directory | Environment | Status |
|---|---|---|
| `onprem/` | Local k3s via OrbStack | Active |
| `aws/` | EKS | In progress |
| `azure/` | AKS | Planned |
| `gcp/` | GKE | Planned |

## Related repos
- [jamesmcculley/security-tools](https://github.com/jamesmcculley/security-tools) — Falco rules, OPA policies
- [jamesmcculley/sre-tools](https://github.com/jamesmcculley/sre-tools) — Scripts, dashboards, runbooks
