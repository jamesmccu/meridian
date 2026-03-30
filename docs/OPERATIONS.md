# Operations

Operational runbooks for the Meridian platform. Start here when something is broken.

---

## Daily Operations

### Check platform status

```bash
# On-prem — verify stack is up
cd ~/developer/MERIDIAN/onprem
docker compose ps

# Check logs for errors
docker compose logs --tail=50
```

### Start / stop cloud nodes

AWS and Azure nodes are stopped when not in use to avoid charges.

```bash
# AWS — start
aws ec2 start-instances --instance-ids <instance-id> --region us-east-1

# AWS — stop
aws ec2 stop-instances --instance-ids <instance-id> --region us-east-1
```

GCP e2-micro runs continuously — do not stop it, it is free and hosts the observability plane.

---

## Runbooks

### Vault is sealed

Vault uses KMS auto-unseal. If it appears sealed after a restart, the most likely cause is a network issue reaching KMS.

```bash
# Check Vault status
vault status

# Check KMS connectivity (requires AWS credentials)
aws kms describe-key --key-id <key-id>

# If network is fine, restart the Vault container
docker compose restart vault
```

### Metrics are missing in Grafana

Work backwards through the pipeline:

```bash
# 1. Is VictoriaMetrics reachable?
curl https://victoriametrics.meridian.local:8428/health

# 2. Is the scrape target returning metrics?
curl https://<target>:9100/metrics

# 3. Check VictoriaMetrics scrape errors
curl https://victoriametrics.meridian.local:8428/api/v1/targets | python3 -m json.tool
```

### Logs not appearing in Quickwit

```bash
# 1. Check Vector is running and not erroring
docker compose logs vector --tail=50

# 2. Check Fluent Bit output
docker compose logs fluent-bit --tail=50

# 3. Verify Quickwit is indexing
curl https://quickwit.meridian.local:7280/api/v1/meridian-logs/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "*", "max_hits": 5}'
```

### TLS certificate errors

All internal services use certs signed by the Meridian root CA. See `docs/tls-config-reference.md` for the CA setup.

```bash
# Verify cert is valid and not expired
openssl x509 -in /certs/server.pem -noout -dates

# Verify cert is trusted by the root CA
openssl verify -CAfile /certs/rootCA.pem /certs/server.pem
```

---

## Infrastructure

### SSH access

All nodes are accessed via AWS SSM Session Manager — no SSH keys or open ports required.

```bash
aws ssm start-session --target <instance-id>
```

### Repo location on AWS node

```
~/developer/MERIDIAN/
```

### Environment variables

Platform config is read from environment variables prefixed with `MERIDIAN_`. See `python/meridian-core/src/meridian_core/config.py` for the full list and defaults.

---

## Cost Controls

- Stop AWS t3.micro when not actively working on it
- Azure B1s can run continuously during the free 12-month period
- GCP e2-micro is permanently free — leave it running
- Set AWS billing alerts at $10 and $20 in the console
