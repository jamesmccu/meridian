# Falco Rules — Meridian

Custom detection rules for the Meridian platform. These cover attack paths that are specific to a containerized multi-cloud environment running StageGrid — not trying to replicate the Falco default ruleset, which handles general Linux system activity well enough on its own.

## Philosophy

Start strict, tune based on real noise rather than hypothetical false positives. A few rules are disabled by default (`enabled: false`) because they need a production baseline before they're useful. The comments in each rule explain the tuning decision.

The rule ordering follows the rough priority of concern: container escape is the worst-case scenario, so it's first. Credential access comes next because it's the most likely path after an escape. Network anomalies and crypto mining close it out.

## Rules

| Rule | Category | Priority | NIST Controls | Notes |
|---|---|---|---|---|
| Host Filesystem Mounted from Container | Container Escape | CRITICAL | SI-4, AU-2 | Bind-mount of host root — first step in most escape chains |
| nsenter Used in Container | Container Escape | CRITICAL | SI-4, AU-2 | Namespace entry almost always adversarial in this context |
| Interactive Shell in Privileged Container | Container Escape | CRITICAL | SI-4, AU-2 | TTY check cuts most CI/build noise |
| Shadow File Read | Credential Access | ERROR | SI-4, AU-2, AC-6 | Nothing legitimate reads /etc/shadow in our workloads |
| AWS Credentials File Accessed in Container | Credential Access | ERROR | SI-4, AU-2, IA-5 | Workloads should use IRSA, not file-based creds |
| K8s Service Account Token Read by Unexpected Process | Credential Access | WARNING | SI-4, AU-2, IA-9 | Exception list needs per-service tuning |
| Outbound Connection from Shell or Scripting Runtime | Reverse Shell | CRITICAL | SI-4, AU-2 | Will have false positives from init scripts — monitor first |
| Network Tool Spawned in Workload Container | Lateral Movement | WARNING | SI-4, AU-2 | nc, socat, nmap in app containers |
| Workload Container External Egress on Non-Standard Port | Unexpected Egress | WARNING | SI-4, SC-7, AU-12 | **Disabled** — needs egress baseline before enabling |
| Connection to Known Mining Pool Port | Crypto Mining | CRITICAL | SI-4, AU-2 | Stratum protocol ports |
| Mining Software Executed | Crypto Mining | CRITICAL | SI-4, AU-2 | Binary name + stratum URI detection |

## Disabled Rules

**Workload Container External Egress on Non-Standard Port** is disabled by default. It fires on anything making an outbound connection outside of 80/443 — package registries, telemetry, init containers pulling configs — and without a per-environment allowlist it's more noise than signal. Enable it after running the stack for a week and cataloging the normal egress pattern. The comment in the rule tracks this.

## What's Not Covered Yet

- kubectl exec lateral movement detection — can detect the syscalls but haven't found a clean way to differentiate from legitimate `kubectl exec` debugging sessions without tagging namespaces.
- Vault token abuse — detecting abnormal Vault API access patterns requires correlating at the HTTP layer, which means either a Vault audit device rule or an external SIEM query, not Falco.
- Image pull from unexpected registry — this is better handled by OPA admission policy (see `security/opa/`) than at the Falco layer.

## Loading These Rules

Load alongside the default Falco ruleset, not as a replacement:

```yaml
# falco.yaml
rules_file:
  - /etc/falco/falco_rules.yaml
  - /etc/falco/rules.d/meridian-rules.yaml
```

The Meridian rules reference some macros (`container_not_host`, `rfc1918_or_loopback`) that are defined in `meridian-rules.yaml` itself and don't depend on the default ruleset.

## TODO

- Wire alerts into alert-router once that's built — currently Falco is logging to stdout and that's it.
- Add a rule for unexpected process spawns in the Vault container — the Vault binary shouldn't be forking anything.
