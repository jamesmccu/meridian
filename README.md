# Meridian

**Cloud security and observability platform — built to show how security engineering, network security, and SRE converge in multi-cloud environments.**

Meridian models a realistic enterprise security posture across AWS and GCP. It covers the full stack from network segmentation and identity management through runtime threat detection, vulnerability scanning, and centralized observability — the kind of work that falls between "security engineer" and "SRE" at most companies and usually belongs to whoever understands both.

> Built by [James McCulley](https://jamesmcculley.dev) — Senior SRE / Security Engineer  
> GitHub: [github.com/jamesmcculley](https://github.com/jamesmcculley)

This README reflects the intended architecture. See [Status](#status) for what's actually running.

---

## Why This Project Exists

Most portfolio infrastructure projects deploy a generic app and call it done. This one is different. Meridian models a fictional company (Meridian Software, an AI hardware manufacturer) running a production workload — **StageGrid**, a live-events ticketing platform. StageGrid's traffic profile — sharp on-sale spikes, high checkout criticality, async notification fanout — forces real decisions about security boundaries, failure domain isolation, SLO design, and compliance scope.

The goal is to show how I think about securing and operating cloud infrastructure end-to-end, not just which tools I can install.

---

## Architecture

### Cloud Placement

Each cloud is used for its genuine strengths. Multi-cloud here is an architectural decision, not a checkbox.

| Function | Provider | Why |
|---|---|---|
| **Security & Secrets** | AWS | KMS auto-unseal for Vault, IAM-native auth, GuardDuty for threat detection, Security Hub for posture management |
| **Observability & Compute** | GCP | Strong data networking, cost-effective egress, Cloud Armor for edge security |

Azure (Entra ID) is referenced for workload identity federation concepts but is not a deployed plane — keeping scope realistic for a portfolio build.

### Network Security

Network architecture is a first-class concern, not an afterthought.

- **VPC segmentation** — dedicated security, observability, and workload subnets per cloud with least-privilege security group rules
- **Cross-cloud connectivity** — WireGuard mesh between AWS and GCP with mTLS overlay (Linkerd) for service-to-service encryption
- **Ingress controls** — Cloud Armor (GCP) and AWS WAF for edge protection, no direct public access to workloads
- **Network policy enforcement** — Kubernetes NetworkPolicies + Calico for pod-level microsegmentation
- **DNS security** — split-horizon DNS, DNSSEC where supported
- **Flow logging** — VPC Flow Logs (AWS/GCP) fed into observability pipeline for network anomaly detection

### Identity & Access Management

- **Workload identity** — no long-lived credentials anywhere. AWS IRSA for pod-level IAM, GCP Workload Identity for service accounts
- **Secrets management** — HashiCorp Vault with short-lived dynamic credentials for database and cloud API access (Shamir unseal / file storage currently; AWS KMS auto-unseal planned for cloud migration)
- **Service mesh identity** — Linkerd mTLS provides cryptographic service identity without managing certificates manually
- **RBAC** — Kubernetes RBAC + OPA/Gatekeeper policies enforcing namespace isolation, image provenance, and resource constraints
- **Human access** — break-glass procedures documented, no standing admin access to production namespaces

### Security Stack

| Layer | Tool | What It Does |
|---|---|---|
| Runtime threat detection | Falco (eBPF) | Detects anomalous syscalls, container escapes, unexpected network connections — rules in [jamesmcculley/security-tools](https://github.com/jamesmcculley/security-tools) |
| Policy enforcement | OPA / Gatekeeper | Blocks non-compliant deployments (unsigned images, privilege escalation, missing labels) — policies in [jamesmcculley/security-tools](https://github.com/jamesmcculley/security-tools) |
| Vulnerability scanning | Trivy | Container image CVE scanning in CI and on-cluster admission |
| Cloud threat detection | GuardDuty | AWS-native detection for compromised credentials, crypto mining, recon activity |
| Cloud posture | Security Hub | Aggregated compliance findings across AWS accounts |
| Secrets management | Vault | Dynamic secrets with TTL-based auto-rotation, PKI certificate issuance |

### Observability

Observability feeds security. Anomaly detection, audit trails, and incident response all depend on good telemetry.

| Signal | Tool | Notes |
|---|---|---|
| Metrics | VictoriaMetrics | Prometheus-compatible, lower resource footprint |
| Logs | Quickwit | Columnar log search, cost-efficient at scale |
| Traces | Jaeger | Distributed tracing for cross-service request flows — planned |
| Collection | OpenTelemetry + Fluent Bit + Vector | OTel for traces/metrics, Fluent Bit for node logs, Vector for routing and enrichment |
| Dashboards | Grafana | Unified view across all signal types |

### StageGrid Services

StageGrid is the workload that creates realistic SRE and security scenarios.

| Service | Responsibility | SLO Target | Status |
|---|---|---|---|
| stagegrid-tickets | Seat reservation and checkout (PCI-scoped) | 99.9% | Building |
| stagegrid-catalog | Event and venue browse | 99.5% | Planned |
| stagegrid-notify | Fan notification fanout | 99.0% | Planned |
| stagegrid-identity | Auth and access control | 99.9% | Planned |
| stagegrid-loadgen | Synthetic traffic generation | — | Planned |

SLO burn rate alerting will fire at 1-hour and 6-hour windows tracked in VictoriaMetrics.

---

## Compliance Mapping

Each security component maps to specific NIST 800-53 control families:

| Component | Controls | Coverage |
|---|---|---|
| Falco | AU-2, AU-6, SI-4 | Audit events, audit review, system monitoring |
| OPA / Gatekeeper | CM-2, CM-6, AC-3 | Baseline config, config settings, access enforcement |
| Vault | IA-5, SC-12, SC-13 | Authenticator management, key establishment, cryptographic protection |
| Linkerd mTLS | SC-8, SC-23, IA-9 | Transmission confidentiality, session authenticity, service identification |
| Trivy | RA-5, SI-2 | Vulnerability monitoring, flaw remediation |
| GuardDuty | SI-4, IR-4 | System monitoring, incident handling |

Additional compliance design targets:
- **PCI-DSS** — stagegrid-tickets is PCI-scoped. Vault manages credentials with short-lived leases and full audit logging. Network policies isolate PCI workloads to dedicated namespaces.
- **SOC2 Type II** — access control, audit logging, and change management controls mapped to ArgoCD (change management) and Vault (access control).

---

## Python Tooling

Platform tooling lives in `tools/`. Written in Python with type hints and async where appropriate.

| Tool | Description | Status |
|---|---|---|
| `meridian-core` | Shared library: config, Vault client, service discovery | Implemented |
| `alert-router` | Alert routing and enrichment (Falco/GuardDuty → Slack/PagerDuty) | Planned |
| `canary-analyzer` | Automated canary analysis using VictoriaMetrics metrics | Planned |
| `flow-analyzer` | VPC Flow Log parsing and network anomaly detection | Planned |
| `py-exporter` | Custom VictoriaMetrics exporter for StageGrid business metrics | Planned |

---

## Deployment & GitOps

- **ArgoCD** — declarative GitOps for all Kubernetes manifests, drift detection, automated sync (App of Apps pattern)
- **Terraform** — infrastructure-as-code for all cloud resources (VPCs, IAM, compute, KMS)
- **CI pipeline** — Trivy image scanning + OPA policy checks run before any manifest reaches ArgoCD

---

## Repository Structure

```
meridian/
├── .github/workflows/              # CI: build+sign, lint, trivy scan, manifest validation
├── aws/vault/config/               # Vault config for AWS plane (planned)
├── compliance/
│   └── nist-800-53-mapping.md      # NIST 800-53 control mapping
├── docs/
│   └── THREAT-MODEL.md             # STRIDE threat model
├── gitops/
│   ├── argocd/                     # App of Apps definitions (planned)
│   └── helm/meridian-chart/        # Helm chart scaffold
├── k8s/                            # Kubernetes manifests (planned)
├── networking/
│   ├── calico/                     # Network policies (planned)
│   ├── waf/                        # Cloud Armor / AWS WAF rules (planned)
│   └── wireguard/                  # Cross-cloud mesh (planned)
├── observability/
│   ├── otel/                       # Fluent Bit + Vector pipeline configs
│   ├── quickwit/                   # Index and ingest config
│   └── victoriametrics/            # Scrape config
├── onprem/
│   └── docker-compose.yml          # Running stack: Vault, VictoriaMetrics, Quickwit, Nginx, MongoDB
├── security/
│   ├── falco/rules/                # Custom Falco detection rules
│   ├── opa/templates/              # Gatekeeper ConstraintTemplates
│   ├── opa/constraints/            # Gatekeeper Constraint resources
│   └── trivy/                      # Trivy config
├── terraform/
│   ├── aws/                        # VPCs, IAM, KMS, GuardDuty (planned)
│   └── gcp/                        # VPCs, firewall rules, Cloud Armor (planned)
└── tools/meridian-core/            # Core Python library (implemented)
```

See [STRUCTURE.md](./STRUCTURE.md) for the authoritative directory inventory.

---

## Status

> Last updated: April 2026

### Running

- **Vault** — initialized and unsealed (Shamir unseal, file storage backend); KMS auto-unseal planned for AWS migration
- **VictoriaMetrics** — deployed, ingesting metrics via Node Exporter
- **Quickwit** — deployed for log indexing
- **Vector / Fluent Bit** — log collection and shipping pipeline configured end-to-end
- **Nginx** — TLS reverse proxy
- **MongoDB** — data layer for StageGrid services
- **meridian-core** — Python shared library implemented

### In Progress

- Terraform modules for AWS and GCP VPCs, IAM, and security services
- Falco runtime security rules
- OPA/Gatekeeper admission policies
- ArgoCD GitOps configuration

### Planned

- Network policy enforcement (Calico + Kubernetes NetworkPolicies)
- Cloud Armor / AWS WAF rule sets
- GuardDuty + Security Hub enablement
- Linkerd service mesh with mTLS
- Trivy CI integration (GitHub Actions)
- NIST 800-53 compliance dashboard in Grafana
- VPC Flow Log analysis tooling

---

## What This Demonstrates

This project shows competency across the overlap between security engineering, network security, and site reliability:

- **Security architecture** — defense-in-depth across multiple clouds, not just tool installation
- **Network security** — VPC segmentation, microsegmentation, encrypted transit, WAF/edge protection, flow log analysis
- **Identity & access management** — zero standing privilege, workload identity, dynamic secrets, service mesh identity
- **Cloud security operations** — threat detection, vulnerability scanning, runtime monitoring, compliance mapping
- **Observability as a security function** — metrics, logs, and traces for anomaly detection and incident response
- **Infrastructure as code** — reproducible, auditable infrastructure reviewable like application code
- **Python automation** — custom tooling for alert routing, canary analysis, network analysis, and operational workflows

---

## Cost

Lab cost target is under $15/month. Managed Kubernetes (EKS/GKE) is intentionally avoided — each cloud node runs k3s on a single small VM. This mirrors what a cost-conscious team would do for non-production workloads. Production deployment notes are documented per-component where the path to EKS/GKE is straightforward.

---

## Contact

**James McCulley** — Senior SRE / Security Engineer  
[jamesmcculley.dev](https://jamesmcculley.dev) · [github.com/jamesmcculley](https://github.com/jamesmcculley)

---

## License

MIT