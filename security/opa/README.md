# OPA / Gatekeeper Policies — Meridian

Gatekeeper admission policies for the Meridian Kubernetes cluster. Each policy is split into a ConstraintTemplate (the Rego logic, applied once) and a Constraint resource (the instance that sets match scope and parameters).

Templates live in `templates/`, constraints in `constraints/`.

## Policies

| Policy | File | NIST Controls | Notes |
|---|---|---|---|
| Block privileged containers | `k8s-block-privileged` | CM-6, AC-3, SI-4 | Also blocks dangerous capabilities: SYS_ADMIN, NET_RAW, etc. |
| Require resource limits | `k8s-require-resource-limits` | CM-6, SC-5 | CPU and memory limits required; requests not enforced |
| Restrict image registries | `k8s-restrict-registries` | CM-7, SI-3 | ghcr.io and gcr.io only; Docker Hub excluded |
| Block :latest tag | `k8s-block-latest-tag` | CM-2, CM-6 | Untagged images also blocked |
| Require labels | `k8s-require-labels` | CM-8 | app, team, environment required on all pods |
| Restrict host namespaces | `k8s-restrict-host-namespaces` | SC-7, AC-3 | hostNetwork/hostPID/hostIPC denied; kube-system exempted |

## Enforcement Mode

All constraints use `enforcementAction: deny`. There's no `warn` or `dryrun` mode in these files — the intent is to apply these before any workloads are deployed, not after. If you need to roll these out against an existing cluster, switch to `dryrun` first and check the Gatekeeper audit logs.

## TODO

- Add a Cosign signature verification constraint once we have a signing pipeline wired up end-to-end — could enforce that here but it requires the Cosign verifier sidecar.
- The registry allowlist in `restrict-registries` needs the GCP Artifact Registry path added once that's provisioned.
