# Troubleshooting

Common issues and fixes for the Meridian platform.

---

## Docker / On-Prem Stack

### Container fails to start

```bash
# Check logs for the specific container
docker compose logs <service> --tail=100

# Check if port is already in use
ss -tlnp | grep <port>

# Restart a single service
docker compose restart <service>
```

### docker compose up fails with "permission denied"

```bash
# Check file ownership
ls -la

# Fix ownership if needed
sudo chown -R $USER:$USER .
```

### Container starts but service is unreachable

```bash
# Verify the container is actually healthy
docker compose ps

# Check what port it's listening on inside the container
docker compose exec <service> ss -tlnp

# Verify the port mapping
docker compose port <service> <container-port>
```

---

## TLS Issues

### "certificate signed by unknown authority"

The Meridian root CA is not trusted by the client. Add it to the trust store or pass it explicitly.

```bash
# Pass CA cert explicitly with curl
curl --cacert /certs/rootCA.pem https://service.meridian.local:8200

# Add to system trust store (Amazon Linux)
sudo cp /certs/rootCA.pem /etc/pki/ca-trust/source/anchors/meridian-root-ca.pem
sudo update-ca-trust
```

### "certificate has expired or is not yet valid"

```bash
# Check cert dates
openssl x509 -in /certs/server.pem -noout -dates

# Check system clock — mismatched time causes false cert failures
timedatectl status
```

---

## Git

### Push rejected — remote moved

```bash
# Update remote URL to current location
git remote set-url origin git@github.com:jamesmcculley/meridian.git
git remote -v  # verify
```

### SSM session loses git config

Git identity is set per-user. If a new SSM session loses it:

```bash
git config --global user.name "James McCulley"
git config --global user.email "your@email.com"
```

---

## AWS / SSM

### SSM Agent unable to acquire credentials

```
AccessDeniedException: Systems Manager's instance management role is not configured
```

Enable Default Host Management Configuration in Fleet Manager, or attach `AmazonSSMManagedInstanceCore` to the instance profile. See AWS docs for DHMC setup.

### Instance hostname shows IP instead of hostname

```bash
# Verify hostname was set
hostnamectl status

# If set but prompt still shows IP, reload shell
exec bash

# If PS1 is being overridden by /etc/profile.d
grep -r 'PS1' /etc/profile.d/
```

---

## Python Tooling

### Import errors running meridian-core tools

```bash
# Verify you're in the right directory
pwd

# Install the package in development mode
cd python/meridian-core
pip install -e . --break-system-packages
```

### Tests failing unexpectedly

```bash
# Run with verbose output to see which test and why
pytest -v

# Run a single test file
pytest tests/test_config.py -v
```
