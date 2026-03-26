# Meridian — TLS Config Reference

> All services use the mkcert wildcard cert at `./certs/meridian.local.pem` and CA at `./certs/rootCA.pem`.  
> Mount `./certs:/certs:ro` on every Compose service.  
> See Phase 0 of the Day 1 checklist for cert generation steps.

---

## 1. Vault — vault.hcl (TLS, not dev mode)

```hcl
ui = true

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/certs/meridian.local.pem"
  tls_key_file  = "/certs/meridian.local-key.pem"
}

storage "file" {
  path = "/vault/data"
}

api_addr     = "https://vault.meridian.local:8200"
cluster_addr = "https://vault.meridian.local:8201"
```

**docker-compose.yml snippet:**
```yaml
vault:
  image: hashicorp/vault:latest
  cap_add: [IPC_LOCK]
  volumes:
    - ./certs:/certs:ro
    - ./vault/config:/vault/config:ro
    - ./data/vault:/vault/data
  command: vault server -config=/vault/config/vault.hcl
  environment:
    VAULT_ADDR: https://vault.meridian.local:8200
```

**Homelab migration:** swap `storage "file"` for `storage "raft"` with peer addresses. No other changes.

---

## 2. node_exporter — web.yml + scrape config

**web.yml** (mounted at `/etc/node_exporter/web.yml`):
```yaml
tls_server_config:
  cert_file: /certs/meridian.local.pem
  key_file:  /certs/meridian.local-key.pem
```

**docker-compose.yml snippet:**
```yaml
node-exporter:
  image: prom/node-exporter:latest
  volumes:
    - ./certs:/certs:ro
    - ./node-exporter/web.yml:/etc/node_exporter/web.yml:ro
  command:
    - --web.config.file=/etc/node_exporter/web.yml
```

**VictoriaMetrics scrape_config snippet** (in `prometheus.yml`):
```yaml
scrape_configs:
  - job_name: node
    scheme: https
    tls_config:
      ca_file:   /certs/rootCA.pem
      cert_file: /certs/meridian.local.pem
      key_file:  /certs/meridian.local-key.pem
    static_configs:
      - targets: [node-exporter:9100]
```

---

## 3. Fluent Bit → Vector (TLS forward)

**fluent-bit.conf output section:**
```ini
[OUTPUT]
    Name          forward
    Match         *
    Host          vector
    Port          24224
    tls           on
    tls.ca_file   /certs/rootCA.pem
    tls.crt_file  /certs/meridian.local.pem
    tls.key_file  /certs/meridian.local-key.pem
```

**vector.yaml source section:**
```yaml
sources:
  fluent_in:
    type: fluent
    address: 0.0.0.0:24224
    tls:
      enabled:  true
      ca_file:  /certs/rootCA.pem
      crt_file: /certs/meridian.local.pem
      key_file: /certs/meridian.local-key.pem
```

---

## 4. Vector → Quickwit (HTTPS sink)

**vector.yaml sink section:**
```yaml
sinks:
  quickwit_out:
    type: http
    inputs: [fluent_in]
    uri: https://quickwit.meridian.local:7280/api/v1/meridian-logs/ingest
    encoding:
      codec: json
    tls:
      ca_file: /certs/rootCA.pem
    request:
      headers:
        content-type: application/json
```

---

## 5. VictoriaMetrics — full scrape tls_config

Add to every job in `prometheus.yml` under VictoriaMetrics:
```yaml
tls_config: &tls_defaults
  ca_file:   /certs/rootCA.pem
  cert_file: /certs/meridian.local.pem
  key_file:  /certs/meridian.local-key.pem

scrape_configs:
  - job_name: node
    scheme: https
    tls_config: *tls_defaults
    static_configs:
      - targets: [node-exporter:9100]

  - job_name: victoriametrics
    scheme: https
    tls_config: *tls_defaults
    static_configs:
      - targets: [victoriametrics:8428]

  - job_name: quickwit
    scheme: https
    tls_config: *tls_defaults
    static_configs:
      - targets: [quickwit:7280]
```

> Note: YAML anchors (`&tls_defaults` / `*tls_defaults`) keep the config DRY. All scrape targets share the same TLS block.

---

## 6. MongoDB — TLS connection

**docker-compose.yml snippet:**
```yaml
mongo:
  image: mongo:7
  volumes:
    - ./certs:/certs:ro
    - ./data/mongo:/data/db
  command: >
    mongod
    --tlsMode requireTLS
    --tlsCertificateKeyFile /certs/meridian.local.pem
    --tlsCAFile /certs/rootCA.pem
```

**Connection string (local):**
```
mongodb://localhost:27017/?tls=true&tlsCAFile=/path/to/certs/rootCA.pem
```

**atlas-ops Python (motor async):**
```python
import motor.motor_asyncio
import os

client = motor.motor_asyncio.AsyncIOMotorClient(
    os.environ["MONGO_URI"],
    tls=True,
    tlsCAFile="/certs/rootCA.pem",
)
```

> `MONGO_URI` is read from Vault. For Atlas, the `tlsCAFile` arg is omitted — Atlas uses a public CA already trusted by the system.

---

## 7. Vault — environment variables for all services

All services that talk to Vault set:
```bash
VAULT_ADDR=https://vault.meridian.local:8200
VAULT_CACERT=/certs/rootCA.pem
```

In Compose:
```yaml
environment:
  VAULT_ADDR: https://vault.meridian.local:8200
  VAULT_CACERT: /certs/rootCA.pem
```

---

## TLS traffic map

```
Browser
  └─► Traefik (TLS termination) ──► Grafana         (internal HTTPS)
                                ──► Quickwit UI      (internal HTTPS)
                                ──► ArgoCD           (internal HTTPS)
                                ──► Vault UI         (internal HTTPS)
                                ──► Jaeger UI        (internal HTTPS)

VictoriaMetrics scraper
  └─► node_exporter             (HTTPS, web.config.file)
  └─► Quickwit metrics          (HTTPS)
  └─► self-scrape               (HTTPS)

Fluent Bit ──► (TLS forward) ──► Vector ──► (HTTPS) ──► Quickwit

Python tools (meridian-core, atlas-ops, alert-router, etc.)
  └─► Vault                     (HTTPS, VAULT_CACERT set)
  └─► MongoDB local             (mongodb+tls://)
  └─► MongoDB Atlas             (mongodb+srv://, public CA)

k3s pod-to-pod
  └─► Linkerd mTLS              (automatic, all annotated pods)
```

---

## Cert renewal (local)

mkcert certs are valid for ~2 years. To renew:
```bash
mkcert '*.meridian.local' meridian.local
cp meridian.local.pem meridian.local-key.pem ./certs/
docker compose restart
```

cert-manager in k3s handles renewal automatically via the ClusterIssuer.

---

*Part of the Meridian portfolio project. Companion to `meridian-day1-checklist.md`.*
