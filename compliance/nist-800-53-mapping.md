# NIST 800-53 Compliance Mapping — Meridian

I mapped each security component to the NIST 800-53 control families it addresses. Not every control has full implementation yet — the Status column tracks what's real vs. what's designed. Components that are planned are marked as such; this document shouldn't be read as a claim that everything is deployed.

This is a living document. As the cloud planes come up and more components land, the status column will shift. The intent is to show that the architecture was designed with these controls in mind, not to claim compliance certification.

---

| Control ID | Control Name | Meridian Component | Implementation Status | Implementation Notes |
|---|---|---|---|---|
| **AC — Access Control** |||||
| AC-2 | Account Management | Vault + K8s RBAC | Planned | Dynamic credentials via Vault; K8s RBAC manifests pending cluster provisioning |
| AC-3 | Access Enforcement | OPA/Gatekeeper | Implemented | Admission policies enforce namespace isolation, image provenance, resource constraints |
| AC-3 | Access Enforcement | Vault | Implemented | Policy-based access to secrets; short-lived tokens with scoped permissions |
| AC-6 | Least Privilege | Vault | Implemented | Service credentials issued with minimum required permissions and TTL-based expiry |
| AC-6 | Least Privilege | IRSA / Workload Identity | Planned | Pod-level IAM on AWS and GCP — no long-lived credentials |
| AC-17 | Remote Access | WireGuard | Planned | Cross-cloud mesh; no direct SSH to nodes planned |
| **AU — Audit and Accountability** |||||
| AU-2 | Event Logging | Falco | Implemented | syscall-level event logging for container escape, credential access, anomalous exec |
| AU-2 | Event Logging | Vault audit log | Implemented | All Vault API requests logged with request/response metadata |
| AU-6 | Audit Review | Quickwit | Implemented | Log indexing and search; Falco output shipped via Vector/Fluent Bit pipeline |
| AU-9 | Audit Log Protection | Quickwit | Implemented | Centralized log storage separate from workload nodes |
| AU-12 | Audit Record Generation | Vector / Fluent Bit | Implemented | Log collection and routing pipeline configured end-to-end |
| AU-12 | Audit Record Generation | VPC Flow Logs | Planned | Network-layer audit trail; enabled when cloud planes are provisioned |
| **CM — Configuration Management** |||||
| CM-2 | Baseline Configuration | Terraform | Planned | IaC for all cloud resources; modules in `terraform/aws/` and `terraform/gcp/` |
| CM-6 | Configuration Settings | OPA/Gatekeeper | Implemented | Admission policies enforce required labels, resource limits, registry restrictions |
| CM-7 | Least Functionality | OPA/Gatekeeper | Implemented | Block latest tags, block privileged containers, restrict host namespaces |
| CM-8 | System Component Inventory | OPA/Gatekeeper (labels) | Implemented | Required `app`, `team`, `environment` labels on all pods |
| CM-14 | Signed Components | Cosign | Implemented | All meridian-core container images signed via keyless Cosign in CI |
| CM-3 | Configuration Change Control | ArgoCD | Planned | GitOps-driven change management with drift detection |
| **IA — Identification and Authentication** |||||
| IA-5 | Authenticator Management | Vault | Implemented | Dynamic credentials with TTL-based auto-rotation; no static secrets |
| IA-5 | Authenticator Management | IRSA | Planned | AWS pod-level IAM authentication; removes need for AWS access keys in containers |
| IA-9 | Service Identification | Linkerd mTLS | Planned | Cryptographic service identity at the service mesh layer |
| **IR — Incident Response** |||||
| IR-4 | Incident Handling | Falco | Implemented | Real-time detection and alerting for high-priority events |
| IR-4 | Incident Handling | alert-router | Planned | Falco/GuardDuty alert routing to Slack/PagerDuty; see `tools/alert-router/` |
| IR-5 | Incident Monitoring | GuardDuty | Planned | AWS-native threat detection for the security plane |
| IR-6 | Incident Reporting | alert-router | Planned | — |
| **RA — Risk Assessment** |||||
| RA-5 | Vulnerability Monitoring | Trivy | Implemented | CI scanning on every PR: filesystem, image, and config scan modes |
| RA-5 | Vulnerability Monitoring | Dependabot | Implemented | Automated dependency update PRs via GitHub Dependabot |
| **SC — System and Communications Protection** |||||
| SC-7 | Boundary Protection | VPC segmentation | Planned | Dedicated security, observability, and workload subnets per cloud |
| SC-7 | Boundary Protection | WAF | Planned | Cloud Armor (GCP) and AWS WAF for edge ingress; rules in `networking/waf/` |
| SC-7 | Boundary Protection | Calico | Planned | Pod-level network policies; manifests in `networking/calico/` |
| SC-8 | Transmission Confidentiality | Nginx TLS | Implemented | TLS termination at the on-prem ingress via self-signed CA |
| SC-8 | Transmission Confidentiality | Linkerd mTLS | Planned | Service-to-service encryption within the cluster |
| SC-12 | Cryptographic Key Establishment | Vault PKI | Implemented | PKI secrets engine for certificate issuance |
| SC-13 | Cryptographic Protection | Vault | Implemented | AES-256-GCM encryption of secrets at rest in Vault |
| SC-13 | Cryptographic Protection | AWS KMS | Planned | KMS auto-unseal for Vault on AWS migration |
| SC-23 | Session Authenticity | Linkerd mTLS | Planned | see SC-8 / Linkerd above |
| SC-28 | Protection at Rest | Vault | Implemented | All secrets encrypted at rest in Vault's file storage backend |
| **SI — System and Information Integrity** |||||
| SI-2 | Flaw Remediation | Trivy | Implemented | CVE scanning in CI pipeline; CRITICAL/HIGH findings block merge |
| SI-3 | Malicious Code Protection | Falco | Implemented | Runtime detection of mining software, reverse shells, unexpected binaries |
| SI-3 | Malicious Code Protection | Trivy | Implemented | Image scanning for known malicious packages |
| SI-4 | System Monitoring | Falco | Implemented | see `security/falco/` for full rule coverage |
| SI-4 | System Monitoring | GuardDuty | Planned | AWS-native anomaly detection for the security plane |
| SI-4 | System Monitoring | VictoriaMetrics | Implemented | Metrics pipeline for anomaly detection once alerting rules are configured |
