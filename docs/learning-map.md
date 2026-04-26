# Learning Map

Meridian is structured around a specific competency target: becoming proficient
across platform engineering, security engineering, and SRE fundamentals.

## Competency Mapping

| Area | What Meridian Should Demonstrate |
|---|---|
| Python DSA | Platform tools that parse, aggregate, search, rank, and analyze operational data. |
| Linux internals | Host process, network, filesystem, cgroup, journald, auditd, and eBPF visibility. |
| Kubernetes | Cluster operations, workloads, ingress, secrets, storage, policies, and operators. |
| System design | Clear architecture docs, ADRs, tradeoffs, trust boundaries, failure modes, and capacity assumptions. |
| Distributed systems | Representative services with queues, retries, idempotency, tracing, backpressure, and failure injection. |
| Observability | Metrics, logs, traces, dashboards, alerts, SLOs, and telemetry routing. |
| Security tooling | Secrets, scanning, signing, policy, runtime detection, host auditing, and cloud findings. |
| GitOps/IaC | Declarative infrastructure, CI validation, GitOps reconciliation, and reproducible deployments. |
| Multi-cloud | Provider-specific IAM, KMS, DNS, object storage, and detection services with explicit rationale. |
| Datadog | Selective SaaS telemetry export, APM, dashboards, and cost controls. |

## Python DSA Track

Python should be used for real platform utilities, not isolated toy scripts.

Good Meridian tools:

- `meridianctl`: platform health and inventory CLI.
- `flow-analyzer`: parse and summarize network flow logs.
- `alert-router`: enrich and route alerts.
- `slo-analyzer`: compute error-budget burn from metrics.
- `sarif-summarizer`: summarize Trivy findings and risk acceptance state.

Useful DSA concepts:

- Hash maps for aggregation and indexing.
- Heaps for top-N talkers, highest-error services, and priority alert queues.
- Graph traversal for service dependency maps.
- Sliding windows for rate and burn-rate calculations.
- Tries or prefix trees for route/path analysis.
- Queues for event processing.

## Linux Internals Track

Meridian should include host-level experiments and runbooks around:

- systemd service lifecycle.
- journald collection and forwarding.
- auditd rules and event review.
- cgroups and resource limits.
- network namespaces and iptables/nftables.
- eBPF tracing with bpftrace or Cilium tooling.
- disk pressure and log retention.

## Kubernetes Track

Recommended progression:

1. Deploy k3s in the homelab.
2. Package platform services with Helm.
3. Reconcile platform state with Argo CD or Flux.
4. Add ingress and TLS automation.
5. Add secrets integration.
6. Add network policies.
7. Add runtime security and admission control.
8. Add representative hosted services.
9. Add backup, restore, and disaster recovery drills.

## Observability Track

The observability stack should answer operational questions:

- Is the platform healthy?
- Which service is failing?
- What changed recently?
- Are errors user-facing or internal?
- Is the issue compute, network, storage, dependency, or deployment related?
- Which security events happened before or during the incident?

Recommended components:

- VictoriaMetrics for metrics.
- Grafana for dashboards.
- Quickwit or Loki for logs.
- Tempo or Jaeger for traces.
- OpenTelemetry Collector for routing.
- Blackbox exporter or equivalent for external checks.
- Optional Datadog Agent for SaaS comparison.

## Security Track

Security tooling should exist at multiple stages:

| Stage | Controls |
|---|---|
| Source | dependency review, secret scanning, linting |
| Build | Trivy, SBOM, image signing |
| Registry | signed artifacts, immutable tags where practical |
| Admission | OPA/Gatekeeper or Kyverno policies |
| Runtime | Falco, auditd, Cilium/Hubble visibility |
| Secrets | Vault, short-lived credentials where practical |
| Cloud | GuardDuty, Security Hub, IAM Access Analyzer |

## GitOps/IaC Track

Recommended ownership:

- Ansible: homelab host bootstrap.
- OpenTofu/Terraform: cloud resources.
- Helm: reusable Kubernetes packaging.
- Argo CD or Flux: Kubernetes reconciliation.
- SOPS/age or Vault integration: secret delivery.
- GitHub Actions: CI, tests, scans, signing, manifest validation.

## Proof Of Competence

The project should make competence visible through:

- Working deployments.
- Verification commands.
- Diagrams.
- ADRs.
- Runbooks.
- Failure drills.
- Security evidence tables.
- SLO dashboards.
- Clear distinction between implemented and planned work.
