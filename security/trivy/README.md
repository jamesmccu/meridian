# Trivy CI Scanning

Three scan modes run on every PR targeting main:

- **Filesystem scan** (`trivy fs .`) — scans the source tree for vulnerabilities in `pyproject.toml`, lockfiles, and Dockerfile layers. This is the hard gate: CRITICAL and HIGH findings fail the build.
- **Image scan** (`trivy image ghcr.io/jamesmcculley/meridian-detect:latest`) — scans the last published container image from main. This scan is informational on PRs because `:latest` may not exist yet, may not be public, or may represent main rather than the PR.
- **Config scan** (`trivy config .`) — checks docker-compose and any manifests for misconfigurations. Currently informational only (exit-code 0) until we've established a baseline.

Severity threshold is CRITICAL and HIGH for the first two modes. The CVE ignore list in `trivy.yaml` is empty by design — nothing gets ignored until we've explicitly reviewed and accepted a risk.

Results appear in the GitHub Security tab via SARIF upload.
