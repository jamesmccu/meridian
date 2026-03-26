# Meridian — Day 1 Local Setup Checklist

> **Target:** MacBook Pro local build before homelab is ready  
> **Total tasks:** 47 across 9 phases | **Est. time:** ~7 hours  
> **Migration key:** `🟡 migrates` = will move to homelab | `🟢 local only` = Mac forever | `🔵 cloud` = AWS/Azure/Atlas target  
> **FAANG tag:** `⚡ FAANG gap` = closes a gap a senior SRE interviewer would probe  
> **Design principle:** Dev is a 1:1 replica of prod. All traffic encrypted at all hops, no exceptions.

---

## Phase 0 — TLS Foundation (~45 min)

> All subsequent phases inherit from this. Do not skip or defer any task here.

- [ ] **Install mkcert + create local CA** 🟢 local only  
  `brew install mkcert && mkcert -install` — installs a locally-trusted CA into your system keystore. Every service cert is browser/curl trusted from here.

- [ ] **Generate wildcard cert for \*.meridian.local** 🟢 local only  
  `mkcert '*.meridian.local' meridian.local` — one cert covers all services. Add `meridian.local` to `/etc/hosts` pointing to `127.0.0.1`.

- [ ] **Copy mkcert CA + wildcard cert into shared Compose certs volume** 🟢 local only  
  `mkdir -p ./certs && cp "$(mkcert -CAROOT)/rootCA.pem" ./certs/ && cp ./_wildcard.meridian.local.pem ./certs/meridian.local.pem && cp ./_wildcard.meridian.local-key.pem ./certs/meridian.local-key.pem`  
  Mount `./certs:/certs:ro` in every Compose service — single source of truth for all TLS material.

- [ ] **Deploy cert-manager to OrbStack k3s** ⚡ FAANG gap | 🟡 migrates  
  `helm install cert-manager jetstack/cert-manager -n cert-manager --create-namespace --set installCRDs=true`

- [ ] **Create ClusterIssuer backed by mkcert CA** ⚡ FAANG gap | 🟡 migrates  
  Secret containing mkcert CA key + cert. In prod this issuer swaps to Let's Encrypt — same manifests, different issuer. Classic hybrid pattern.

- [ ] **Configure Traefik as TLS-terminating ingress** ⚡ FAANG gap | 🟡 migrates  
  OrbStack ships Traefik. Add `IngressRoute` for each service with TLS block referencing cert-manager issuer. All services get `https://` from day one.

- [ ] **Configure Vault with TLS listener (not dev mode)** ⚡ FAANG gap | 🟡 migrates  
  Run Vault with a proper HCL config file + mkcert cert. Eliminates the HTTP listener entirely. See `meridian-tls-config-reference.md` for config snippet.

- [ ] **Configure node_exporter with TLS** ⚡ FAANG gap | 🟡 migrates  
  `--web.config.file=/etc/node_exporter/web.yml` pointing at mkcert cert. VictoriaMetrics scrape config gets matching `tls_config` block. See reference file.

- [ ] **Configure Fluent Bit → Vector with TLS** ⚡ FAANG gap | 🟡 migrates  
  Fluent Bit `forward` output: `tls on` + `tls.ca_file`. Vector `fluent` source: `tls.enabled: true`. Both reference mkcert CA. See reference file.

- [ ] **Configure Vector → Quickwit with TLS** ⚡ FAANG gap | 🟡 migrates  
  Vector HTTP sink gets `tls.ca_file` pointing at mkcert CA. Ensures Vector validates the cert rather than skipping verification. See reference file.

- [ ] **Configure VictoriaMetrics scrape tls_config** ⚡ FAANG gap | 🟡 migrates  
  All `scrape_configs` targets get a `tls_config` block referencing mkcert CA + wildcard cert. See reference file.

- [ ] **Smoke test: confirm zero plain HTTP between all Compose services** 🟢 local only  
  `docker compose up -d && docker compose exec vector curl -v http://quickwit:7280` should refuse. All inter-service calls must use `https://`.

---

## Phase 1 — Homebrew + Core Tooling (~20 min)

- [ ] **Install Homebrew if needed** 🟢 local only  
  `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

- [ ] **Install OrbStack** 🟡 migrates  
  `brew install orbstack` — k3s + Docker with low overhead on Apple Silicon.

- [ ] **Install Terraform via tfenv** 🟡 migrates  
  `brew install tfenv && tfenv install latest && tfenv use latest`

- [ ] **Install kubectl + Helm** 🟡 migrates  
  `brew install kubectl helm`

- [ ] **Install act (GitHub Actions local runner)** 🟢 local only  
  `brew install act` — test workflows without pushing.

---

## Phase 2 — Python Environment (~15 min)

- [ ] **Install pyenv + Python 3.12** 🟢 local only  
  `brew install pyenv && pyenv install 3.12 && pyenv global 3.12`

- [ ] **Create meridian virtualenv** 🟢 local only  
  `python -m venv ~/.venvs/meridian && source ~/.venvs/meridian/bin/activate`

- [ ] **Scaffold pyproject.toml for meridian-core** 🟢 local only  
  Type hints, pydantic, pytest, async/await — senior pattern baseline for all 5 Python tools.

---

## Phase 3 — Secrets Management / Vault (~30 min)

> ⚡ All tasks in this phase close FAANG gaps. Vault is positioned before observability intentionally — credentials come from Vault from the first Compose file, never retrofitted.

- [ ] **Add Vault to Docker Compose (TLS, not dev mode)** ⚡ FAANG gap | 🟡 migrates  
  Uses HCL config file with `tls_cert_file` / `tls_key_file` from `./certs`. No `VAULT_DEV_ROOT_TOKEN_ID`. See reference file for full config.

- [ ] **Store all service credentials in Vault** ⚡ FAANG gap | 🟡 migrates  
  `vault kv put secret/meridian/mongo uri=...` — `MONGO_URI`, Atlas creds, Grafana admin password. No plaintext env vars anywhere.

- [ ] **Deploy Vault Agent Sidecar Injector to k3s** ⚡ FAANG gap | 🟡 migrates  
  `helm install vault hashicorp/vault --set injector.enabled=true` — pods annotate for secret injection, no app code changes needed.

- [ ] **Deploy External Secrets Operator** ⚡ FAANG gap | 🔵 cloud  
  ESO bridges Vault (local) and AWS Secrets Manager (cloud). Same `ExternalSecret` manifest works in both environments.

---

## Phase 4 — Observability Stack / Docker Compose (~30 min)

- [ ] **Write docker-compose.yml with VictoriaMetrics** 🟡 migrates  
  Single-node on port `8428`. Use relative `./data/` volumes — NAS migration is a path swap. TLS config inherited from Phase 0 certs volume.

- [ ] **Add Grafana to Compose** 🟡 migrates  
  Port `3000`, TLS via Traefik ingress, provision VictoriaMetrics datasource via YAML with `tlsSkipVerify: false`.

- [ ] **Add node_exporter for Mac host metrics** 🟡 migrates  
  TLS enabled via `web.yml` from Phase 0. VictoriaMetrics scrapes over HTTPS.

- [ ] **Define SLO recording rules in VictoriaMetrics** ⚡ FAANG gap | 🟡 migrates  
  `availability = 1 - (error_rate / total_rate)`. Wire to Grafana SLO dashboard with error budget burn alerts. FAANG SRE interviews almost always probe this.

- [ ] **Create Grafana SLO dashboard with error budget panel** ⚡ FAANG gap | 🟡 migrates  
  Error budget remaining % + burn rate alert thresholds (1h, 6h, 3d windows). Shows SRE maturity immediately.

- [ ] **docker compose up -d and verify all services on https://** 🟢 local only  
  Confirm Grafana at `https://grafana.meridian.local`, Quickwit at `https://quickwit.meridian.local`, etc.

---

## Phase 5 — Log Pipeline / Fluent Bit → Vector → Quickwit (~45 min)

- [ ] **Add Quickwit to Compose** 🟡 migrates  
  Port `7280` HTTPS only. Init index `meridian-logs`. Volume maps to NAS path later.

- [ ] **Add Vector to Compose** 🟡 migrates  
  TLS on both fluent source (from Fluent Bit) and HTTP sink (to Quickwit). See reference file.

- [ ] **Add Fluent Bit to Compose** 🟡 migrates  
  `forward` output with `tls on`. Tail `/var/log` via volume mount or pipe synthetic logs from Python tools.

- [ ] **Add backpressure config to Vector** ⚡ FAANG gap | 🟡 migrates  
  Set disk buffer + `overflow: drop_newest` policy. Interviewers probe pipeline resilience — this closes that gap directly.

- [ ] **Verify end-to-end log ingest over HTTPS** 🟢 local only  
  `curl --cacert ./certs/rootCA.pem https://quickwit.meridian.local/api/v1/meridian-logs/search?query=*`

---

## Phase 6 — OrbStack k3s + ArgoCD + Service Mesh (~45 min)

- [ ] **Start OrbStack k3s cluster** 🟡 migrates  
  `orb create k8s meridian` — kubeconfig auto-set.

- [ ] **Install ArgoCD via Helm** 🟡 migrates  
  `helm install argocd argo/argo-cd -n argocd --create-namespace`

- [ ] **Create meridian Git repo + initial app manifests** 🟡 migrates  
  Repo structure used when homelab nodes join — set it right now so nothing needs restructuring later.

- [ ] **Install Linkerd service mesh** ⚡ FAANG gap | 🟡 migrates  
  `brew install linkerd && linkerd install --crds | kubectl apply -f - && linkerd install | kubectl apply -f -`  
  Lighter than Istio, FAANG-grade mTLS. Automatic mutual TLS between all pods.

- [ ] **Annotate meridian namespace for Linkerd injection** ⚡ FAANG gap | 🟡 migrates  
  `kubectl annotate ns meridian linkerd.io/inject=enabled` — zero-trust baseline established automatically for all pods in namespace.

- [ ] **Verify mTLS with linkerd viz** ⚡ FAANG gap | 🟢 local only  
  `linkerd viz install | kubectl apply -f - && linkerd viz dashboard` — confirms all inter-service traffic is encrypted in mesh.

---

## Phase 7 — Security Layer (~40 min)

- [ ] **Install Trivy CLI** 🟢 local only  
  `brew install trivy` — scan images and IaC, no Linux dependency.

- [ ] **Run Trivy against all Compose images** 🟢 local only  
  `trivy image victoriametrics/victoria-metrics:latest` etc. — clean CVE baseline before first deploy.

- [ ] **Deploy OPA/Gatekeeper to k3s** 🟡 migrates  
  `helm install gatekeeper opa/gatekeeper -n gatekeeper-system --create-namespace`

- [ ] **Write ConstraintTemplate: disallow latest tag** 🟡 migrates  
  Maps to SOC2 CC6.1. Concrete control → policy → enforcement chain is a strong interview story.

- [ ] **Write ConstraintTemplate: require resource limits** ⚡ FAANG gap | 🟡 migrates  
  Maps to SOC2 CC6.2 / availability controls. Two policies = a pattern, not a one-off.

- [ ] **Add Falco to Compose (limited mode)** 🟡 migrates  
  Test rule syntax and alert routing before homelab. Kernel module features deferred to Linux node.

- [ ] **Wire Falco + Trivy alerts into alert-router** 🟡 migrates  
  `alert-router` → log to Quickwit (HTTPS) + metric to VictoriaMetrics (HTTPS) + Vault for any rotated secrets.

- [ ] **Add toxiproxy chaos experiment** ⚡ FAANG gap | 🟢 local only  
  `brew install shopify/shopify/toxiproxy` — simulate MongoDB latency/outage. Validate SLO burn rate alerts fire correctly under failure. Proves observability works, not just exists.

---

## Phase 8 — MongoDB Local + Atlas Bootstrap (~25 min)

- [ ] **Add MongoDB to Docker Compose (TLS enabled)** 🟡 migrates  
  `mongo:7` with TLS cert from `./certs`. Connection string uses `mongodb+tls://`. Consistent with Atlas TLS requirement from day one.

- [ ] **Create meridian operational database** 🟡 migrates  
  `mongosh --tls --tlsCAFile ./certs/rootCA.pem: use meridian` — collections: `pipeline_state`, `alert_events`, `scan_results`, `slo_snapshots`.

- [ ] **Scaffold atlas-ops Python tool** 🔵 cloud  
  `pymongo` + `motor` (async). `MONGO_URI` env var read from Vault — local Compose URI in dev, Atlas URI in prod. Same code, two environments.

- [ ] **Register free Atlas M0 cluster** ⚡ FAANG gap | 🔵 cloud  
  [atlas.mongodb.com](https://atlas.mongodb.com) — create `meridian-prod` cluster, grab connection string, store in Vault not in `.env`.

- [ ] **Verify local → Atlas URI swap via Vault** ⚡ FAANG gap | 🔵 cloud  
  `vault kv put secret/meridian/mongo uri=mongodb+srv://...` — `atlas-ops` reads from Vault, not hardcoded env var. Same code path, two backing stores.

---

## Summary

| Phase | Focus | Est. | FAANG gaps |
|---|---|---|---|
| 0 | TLS foundation | 45 min | 8 |
| 1 | Core tooling | 20 min | 0 |
| 2 | Python env | 15 min | 0 |
| 3 | Vault / secrets | 30 min | 4 |
| 4 | Observability | 30 min | 2 |
| 5 | Log pipeline | 45 min | 1 |
| 6 | k3s + mesh | 45 min | 3 |
| 7 | Security | 40 min | 2 |
| 8 | MongoDB + Atlas | 25 min | 3 |
| **Total** | | **~7 hrs** | **23 / 47** |

---

## Migration notes

- All `./data/` and `./certs/` volume paths in Compose are relative — NAS migration is a `rsync` + path update, no config rewrite.
- `MONGO_URI` and all credentials live in Vault from Phase 3 onward. Swapping local → Atlas is a single `vault kv put` command.
- cert-manager `ClusterIssuer` swaps from mkcert CA (local) to Let's Encrypt (homelab/prod) with no manifest changes to services.
- ArgoCD repo structure is final from day one — homelab nodes join as additional clusters, not a restructure.
- Linkerd mesh scales from single OrbStack node to multi-node homelab cluster automatically via the namespace annotation.
- Every service uses the same `./certs` volume — rotating certs on homelab means replacing files in one place, all services pick up on restart.

---

## TLS coverage map

| Traffic hop | Method | Status |
|---|---|---|
| Browser → services | Traefik ingress TLS termination | ✅ Phase 0 |
| Fluent Bit → Vector | mkcert cert, `tls on` | ✅ Phase 0 |
| Vector → Quickwit | mkcert CA, HTTP sink TLS | ✅ Phase 0 |
| VictoriaMetrics → scrape targets | `tls_config` block | ✅ Phase 0 |
| node_exporter listener | `web.yml` TLS config | ✅ Phase 0 |
| App → Vault | HCL `tls_cert_file` listener | ✅ Phase 0 |
| App → MongoDB (local) | `mongodb+tls://` + mkcert CA | ✅ Phase 8 |
| App → MongoDB Atlas | `mongodb+srv://` (TLS required) | ✅ Phase 8 |
| Pod → pod (k3s) | Linkerd mTLS | ✅ Phase 6 |
| etcd ↔ API server (k3s) | k3s default TLS | ✅ out of box |

---

*Generated as part of the Meridian portfolio project — hybrid observability platform targeting MongoDB Staff SRE Observability role.*
*See companion file: `meridian-tls-config-reference.md`*
