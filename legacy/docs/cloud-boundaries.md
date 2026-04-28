# Cloud Boundaries

Meridian should use cloud services deliberately. The default runtime target is
the homelab. Cloud is added where it teaches cloud-native platform and security
concepts that are difficult to reproduce accurately on-premises.

## Cloud Decision Rule

Use the homelab when the goal is to understand the system substrate:

- Linux behavior.
- Kubernetes operations.
- Storage and backup failure modes.
- Network policy and ingress behavior.
- Local observability pipelines.
- Runtime security tooling.

Use cloud when the goal is to understand provider-native primitives:

- IAM and workload identity.
- KMS and envelope encryption workflows.
- Public DNS and domain control.
- Durable object storage.
- Managed security findings.
- Edge exposure and WAF patterns.
- Multi-cloud identity and trust boundaries.

## AWS First

AWS is the recommended first cloud integration because it gives strong coverage
across security engineering topics.

| AWS Service | Meridian Use | Reason |
|---|---|---|
| Route 53 | Public DNS for selected hosted services | Teaches authoritative DNS and controlled public exposure. |
| S3 | Backup target for platform data | Teaches durable object storage, lifecycle policy, and recovery workflows. |
| KMS | Encryption and future Vault auto-unseal | Teaches key policy, grants, envelope encryption, and auditability. |
| IAM / OIDC | Workload identity experiments | Teaches least privilege and federated identity. |
| GuardDuty | Managed threat detection | Teaches cloud-native detection and finding triage. |
| Security Hub | Security posture aggregation | Teaches cloud control mapping and evidence review. |
| IAM Access Analyzer | Policy and access review | Teaches external access detection and permission reasoning. |

## GCP Optional

GCP should be added only when it has a specific learning purpose, not just to make
the project multi-cloud.

Good reasons to add GCP:

- Compare workload identity models.
- Compare object storage and IAM behavior.
- Run a small external observer node.
- Practice multi-cloud DNS, routing, or trust boundaries.
- Compare observability integrations.

Weak reasons to add GCP:

- To claim multi-cloud without using provider-specific capabilities.
- To duplicate the same services already running on-premises.
- To increase scope before the AWS and homelab paths are mature.

## Datadog Boundary

Datadog is useful as a professional observability reference point, but it should
not replace the local observability stack.

Recommended model:

- Keep VictoriaMetrics, local logs, and Grafana as the primary homelab view.
- Run the Datadog Agent in Kubernetes only when there are services worth tracing.
- Export selected metrics, logs, and traces to Datadog.
- Document telemetry filtering and cost controls.
- Use Datadog dashboards/APM to compare SaaS operations with local observability.

Reason:

> Local observability proves that the telemetry pipeline is understood. Datadog
> integration proves familiarity with a common commercial platform without hiding
> the underlying collection, routing, and cost tradeoffs.

## Public Exposure

Only selected services should be public-facing. Public exposure should require:

- Documented owner and purpose.
- TLS termination.
- Ingress policy.
- Logging.
- Health checks.
- Rollback plan.
- Backup/restore plan if stateful.
- Security scan coverage.

A static portfolio or documentation site is a suitable first public workload
because it is low risk, useful, and visible enough to validate the platform's
ingress, deployment, and observability story.
