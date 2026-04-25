# Repository Structure

```
meridian/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── build-sign.yml          # Container build + Cosign keyless signing
│       ├── lint.yml                # Ruff linting for tools/
│       ├── trivy-scan.yml          # Trivy security scanning (new)
│       └── validate-manifests.yml  # YAML validation for all manifests
├── aws/
│   └── vault/
│       └── config/vault.hcl        # Vault server config for AWS plane (planned)
├── compliance/                      # (new)
│   └── nist-800-53-mapping.md      # NIST 800-53 control mapping
├── docs/                            # (new)
│   └── THREAT-MODEL.md             # STRIDE threat model for StageGrid
├── gitops/
│   ├── argocd/                      # (new — planned) App of Apps definitions
│   └── helm/
│       └── meridian-chart/
│           ├── Chart.yaml
│           └── values.yaml
├── k8s/                             # (new — planned) Kubernetes manifests
├── networking/                      # (new — planned)
│   ├── calico/                      # Pod-level network policies
│   ├── waf/                         # Cloud Armor / AWS WAF rules
│   └── wireguard/                   # Cross-cloud mesh configs
├── observability/
│   ├── otel/
│   │   ├── fluent-bit.conf
│   │   └── vector.yaml
│   ├── quickwit/
│   │   └── quickwit.yaml
│   └── victoriametrics/
│       └── prometheus.yml
├── onprem/
│   ├── docker-compose.yml           # Running: Vault, VictoriaMetrics, Quickwit, Nginx, MongoDB
│   ├── nginx/nginx.conf
│   ├── node-exporter/web.yml
│   └── vault/config/vault.hcl
├── security/
│   ├── falco/                       # (new)
│   │   ├── README.md
│   │   └── rules/
│   │       └── meridian-rules.yaml  # Custom detection rules
│   ├── opa/                         # (new)
│   │   ├── README.md
│   │   ├── constraints/             # Gatekeeper Constraint resources
│   │   └── templates/               # Gatekeeper ConstraintTemplates (Rego)
│   ├── trivy/                       # (new)
│   │   ├── README.md
│   │   └── trivy.yaml
│   └── README.md
├── terraform/                       # (new — planned)
│   ├── aws/                         # VPCs, IAM, KMS, GuardDuty, Security Hub
│   └── gcp/                         # VPCs, firewall rules, Cloud Armor, Workload Identity
├── tools/
│   └── meridian-core/               # Core Python library — config, Vault client, service discovery
├── CHANGELOG.md
├── README.md
├── RELEASE_NOTES.md
└── STRUCTURE.md
```

## Directory Status

| Directory | Status | Notes |
|---|---|---|
| `onprem/` | Active | docker-compose stack running locally |
| `observability/` | Active | configs deployed in onprem stack |
| `tools/meridian-core/` | Active | Python library with CI pipeline |
| `security/falco/` | New | custom detection rules |
| `security/opa/` | New | Gatekeeper admission policies |
| `security/trivy/` | New | CI scanning workflow and config |
| `compliance/` | New | NIST 800-53 mapping |
| `docs/` | New | threat model |
| `aws/` | Planned | Vault config staged; provisioning pending |
| `terraform/` | Planned | modules not started |
| `k8s/` | Planned | pending cloud plane provisioning |
| `networking/` | Planned | pending k3s cluster |
| `gitops/argocd/` | Planned | pending cluster |
