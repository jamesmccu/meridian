# Meridian

A production-grade hybrid observability and security platform built on Kubernetes, designed to demonstrate real-world SRE engineering at scale. Meridian spans on-premises k3s, AWS EKS, and Azure AKS — with a unified observability pipeline, secrets management, policy enforcement, and runtime security.

> Built as a portfolio project targeting Staff SRE roles in cloud-native infrastructure, observability, and security engineering.

---

## Architecture Overview

```
MacBook (OrbStack k3s)          Cloud (AWS EKS / Azure AKS)
┌─────────────────────────┐     ┌──────────────────────────┐
│  Fluent Bit             │     │  OpenTelemetry Collector  │
│      ↓                  │     │          ↓                │
│  Vector (backpressure)  │────▶│  VictoriaMetrics (remote) │
│      ↓                  │     │  Quickwit (remote)        │
│  Quickwit (indexing)    │     │  Grafana (unified view)   │
│  VictoriaMetrics        │     └──────────────────────────┘
│  Grafana                │
│  Vault (secrets)        │     MongoDB Atlas
│  OPA/Gatekeeper         │     ┌──────────────────────────┐
│  Falco (runtime)        │     │  meridian-context service │
│  Traefik + Linkerd      │     │  (alert enrichment API)   │
└─────────────────────────┘     └──────────────────────────┘
```

All inter-service traffic is encrypted with mkcert-issued TLS certificates. No `insecure_skip_verify`. No plaintext.

---

## Stack

### Observability Pipeline
| Component | Role |
|-----------|------|
| Fluent Bit | Log collection from host and containers |
| Vector | Log routing with disk-backed buffering (256MB, survives downstream outages) |
| Quickwit | Log indexing and full-text search |
| VictoriaMetrics | Metrics storage and Prometheus-compatible scraping |
| Grafana | Unified dashboards across logs, metrics, and traces |
| Jaeger | Distributed tracing |
| OpenTelemetry | Vendor-neutral instrumentation layer |

### Security & Policy
| Component | Role |
|-----------|------|
| Falco | Runtime threat detection (syscall-level) |
| OPA / Gatekeeper | Kubernetes admission control and policy enforcement |
| Trivy / Grype | Container image vulnerability scanning in CI |
| Syft | SBOM generation |
| Gitleaks | Secret scanning in Git history |
| Wazuh | Host-based intrusion detection (Heimdall phase) |
| Suricata | Network IDS/IPS (Heimdall phase) |

### Infrastructure & GitOps
| Component | Role |
|-----------|------|
| k3s (OrbStack) | Local Kubernetes cluster |
| AWS EKS / Azure AKS | Cloud Kubernetes targets |
| Traefik | Ingress controller |
| Linkerd | mTLS service mesh |
| ArgoCD | GitOps continuous delivery |
| Helm | Chart-based deployments |
| GitHub Actions | CI pipeline (image scanning, lint, test) |
| Vault | Secrets management (Shamir unseal, KV v2) |
| cert-manager | Certificate lifecycle management |

### Data & Context
| Component | Role |
|-----------|------|
| MongoDB Atlas | Alert context registry backing store |
| `meridian-context` | FastAPI service — enriches alerts with SLO risk, revenue exposure, blast radius |

---

## Python Tooling

Five production-quality Python tools built with senior patterns: `pydantic v2`, `async/await`, full type hints, `pytest-asyncio`, `pyproject.toml`, `ruff`, `mypy --strict`.

| Tool | Description |
|------|-------------|
| `meridian-core` | Shared configuration and client library |
| `logparse` | Log parsing and structured extraction |
| `py-exporter` | Custom Prometheus metrics exporter |
| `alert-router` | Alert fanout — Quickwit + VictoriaMetrics + PagerDuty |
| `atlas-ops` | MongoDB Atlas operational tooling via the Atlas API |

---

## Compliance

Control mappings for SOC 2 and PCI-DSS implemented across the stack:

- **Encryption in transit** — TLS on all service-to-service communication
- **Secrets management** — Vault KV v2, no plaintext env vars
- **Audit logging** — all access routed through the observability pipeline
- **Runtime security** — Falco detects and alerts on policy violations
- **Supply chain** — SBOM generation and image scanning in every CI run

---

## Key Design Decisions

**Why VictoriaMetrics over Prometheus?**
VM offers better compression, horizontal scalability, and a compatible PromQL API. In a multi-tenant environment it simplifies the remote write story considerably.

**Why Vector between Fluent Bit and Quickwit?**
Vector provides disk-backed buffering with configurable overflow policy. If Quickwit is unavailable, logs queue to disk rather than dropping. Observability that survives its own downstream failures is a core design principle.

**Why MongoDB Atlas for alert context?**
The `meridian-context` service enriches raw alerts with SLO risk scores, revenue exposure estimates, and correlated signals before they reach an on-call engineer. Atlas provides a globally distributed, schema-flexible store that fits the variable shape of alert metadata without a migration cycle every time a new signal type is added.

**TLS everywhere — no exceptions**
All scrape targets use `server_name` SNI overrides so certificate validation is real against `*.meridian.local`, not skipped. The principle: if encryption is cosmetic, it's not encryption.

---

## Project Structure

```
MERIDIAN/
├── docker-compose.yml        # Full local stack
├── prometheus.yml            # VictoriaMetrics scrape config
├── fluent-bit/               # Log collection config
├── vector/                   # Log routing + backpressure
├── nginx/                    # TLS termination + reverse proxy
├── quickwit.yaml             # Log index config
├── vault/                    # Secrets management config
├── node-exporter/            # Host metrics with TLS
├── meridian-core/            # Core Python library
│   ├── src/meridian_core/
│   └── tests/
└── docs/                     # Architecture and runbooks
```

---

## Running Locally

**Prerequisites:** Docker, OrbStack, mkcert, Python 3.12+

```bash
# Generate TLS certificates
mkcert -install
mkdir -p certs
mkcert -cert-file certs/meridian.local.pem \
       -key-file  certs/meridian.local-key.pem \
       "*.meridian.local" meridian.local
cp "$(mkcert -CAROOT)/rootCA.pem" certs/

# Start the stack
docker compose up -d

# Python environment
python3 -m venv .venv && source .venv/bin/activate
pip install -e meridian-core/

# Unseal Vault (after first run)
export VAULT_ADDR=https://vault.meridian.local:8201
export VAULT_CACERT=certs/rootCA.pem
vault operator unseal  # run twice with two of your three unseal keys
```

**Service endpoints (local ports):**

| Service | URL |
|---------|-----|
| Grafana | https://localhost:13000 |
| VictoriaMetrics | https://localhost:18428 |
| Quickwit | https://localhost:17280 |
| Vault | https://localhost:8201 |
| MongoDB | localhost:37017 |

---

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | TLS foundation, cert-manager, Traefik, Linkerd | ✅ Complete |
| 2 | Core observability pipeline (Fluent Bit → Vector → Quickwit → VM → Grafana) | 🔄 In progress |
| 3 | Python tooling (5 tools, senior patterns) | 🔄 In progress |
| 4 | MongoDB Atlas context service | 📋 Planned |
| 5 | Cloud targets (EKS + AKS) | 📋 Planned |
| 6 | Heimdall MDR stack (Wazuh, Suricata, MISP, TheHive) | 📋 Planned |

---

## Author

James McCulley — Senior SRE
