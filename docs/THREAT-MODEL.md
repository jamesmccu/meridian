# StageGrid Threat Model

## System Overview

StageGrid is a multi-tenant live-events ticketing platform operated by Meridian Software. It handles seat reservation and checkout (PCI-scoped), event catalog browsing, fan notifications, and authentication. The platform runs across two cloud planes — AWS for secrets management and security services, GCP for compute and observability — connected by a WireGuard mesh. The major trust boundaries are: internet to cloud ingress, ingress to workload pods, pod to pod within the cluster, AWS to GCP cross-cloud, and human operators to the Kubernetes API.

---

## Threat Categories

### Spoofing

The main concern here is service identity — a compromised workload impersonating another service to access the payment API or identity service. Without cryptographic service identity, anything that can reach the right network address can claim to be any service. This is partially mitigated by planned Linkerd mTLS, which will provide pod-level certificate identity once deployed. Until then, we're relying on Kubernetes NetworkPolicies (planned) and OPA admission controls to limit which pods can be scheduled in sensitive namespaces. The accepted risk is that network-layer controls alone aren't sufficient if a workload is compromised — an attacker with exec access can reach any in-cluster endpoint the compromised pod can reach. This is the highest-priority gap for the Linkerd deployment phase.

### Tampering

Seat availability data, event metadata, and checkout state in MongoDB could be tampered with by any workload that can reach the database. Vault dynamic credentials help here — each service gets a MongoDB credential with exactly the permissions it needs, and credentials expire, limiting the window for abuse. OPA admission policies prevent unauthorized workloads from being scheduled at all. What we don't have yet is MongoDB audit logging or at-rest encryption — so if a credential gets compromised and used to directly modify records, the tamper may not be detectable from the database layer alone. Falco gives us syscall-level visibility on the MongoDB container, but that's a partial compensating control at best. I'm accepting this risk for now because stagegrid-tickets doesn't have production data yet, and the remediation (MongoDB audit + WiredTiger encryption) is in the roadmap.

### Repudiation

Two repudiation scenarios matter here. First: a customer disputes a ticket purchase and claims no record exists. Second: a team member makes an infrastructure change and denies it. For the customer case, Vault's audit log captures all secrets access with request metadata, and the application event log (via Fluent Bit → Quickwit) provides the application-layer trail. For the infrastructure case, once ArgoCD is deployed all cluster changes will go through GitOps with a signed commit trail. The gap right now is VPC Flow Logs — they're not enabled yet, so network-layer activity between services isn't audited. This means a compromised workload making lateral connections would leave a trail in Falco (which watches syscalls) but not at the network layer. The plan is to enable Flow Logs during cloud plane provisioning.

### Information Disclosure

PII (name, email) and payment card data handled by stagegrid-tickets are the highest-risk assets. The mitigation layers are: Vault dynamic credentials with short TTLs (limits blast radius if a credential leaks), OPA admission policies preventing workloads from unknown registries (reduces supply chain risk), and Trivy CI scanning catching known CVEs before deployment. What's not yet in place is PCI namespace isolation — stagegrid-tickets is supposed to run in a dedicated namespace with strict egress controls, but those Calico policies and namespace configuration haven't landed yet. I'm accepting this risk for now because stagegrid-tickets is still in active development and has no real cardholder data. Full PCI segmentation is a deployment-phase requirement, not a development-phase one.

### Denial of Service

StageGrid has a known challenging traffic profile. On-sale events for popular artists drive sharp checkout spikes — potentially 10-50x normal traffic in under a minute — and the stagegrid-tickets service is the critical path. Failure here means lost revenue and poor customer experience, which is why it has the tightest SLO (99.9%).

The main DoS concerns are: volumetric attacks against ingress, resource exhaustion within the cluster, and downstream throttling (Vault lease creation under spike load). Cloud Armor WAF and AWS WAF (both planned) handle the edge. OPA resource limit policies ensure no single pod can exhaust node capacity. The Vault concern is less obvious — during an on-sale spike, every checkout creates or renews a Vault lease, which puts Vault on the critical path for availability. We don't have rate limiting on the Vault API calls yet, and that's worth thinking about before the first load test.

No load testing has been done yet. That's probably the biggest gap in this section — everything above is architecture-level reasoning about resilience, not empirically validated behavior.

### Elevation of Privilege

A container exploit giving an attacker code execution, then escalating to node-level access, then laterally moving to the Kubernetes API or the Vault container, is the worst-case privilege escalation scenario. The current mitigations: Falco eBPF detects container escape patterns (host filesystem mounts, nsenter, privileged container shells), OPA admission policies block the most common container escape prerequisites (privileged mode, dangerous capabilities, host namespace access). What we don't have yet is seccomp profiles — Falco detects anomalous syscalls but doesn't prevent them. Adding seccomp profiles per workload is the next hardening step after getting Falco wired into alerting.

---

## Trust Boundaries

- **Internet → Cloud ingress edge** — WAF (Cloud Armor / AWS WAF) is the planned control; not yet deployed
- **Ingress → StageGrid workload pods** — Nginx TLS termination (implemented on-prem); cloud ingress configuration planned
- **Pod → Pod within cluster** — Linkerd mTLS (planned); currently unrestricted within-cluster communication
- **AWS → GCP** — WireGuard mesh (planned); security plane to compute/observability plane
- **Operator → Kubernetes API** — Vault authentication + K8s RBAC (planned); no standing admin access design documented
- **CI/CD → Kubernetes cluster** — ArgoCD GitOps (planned); Cosign image signing (implemented) establishes the chain of custody from code to image

---

## Open Risks

**No WAF deployed yet.** The cluster boundary is protected by security groups and planned Calico policies, but there's no Layer 7 inspection at the edge. Cloud Armor and AWS WAF rules are designed (see `networking/waf/`) but not deployed. Until those land, rate limiting and bot mitigation are not in place. The mitigation window depends on when the GCP and AWS planes are provisioned.

**WireGuard mesh keys are rotated manually.** When the cross-cloud WireGuard link is set up, key rotation will be a manual operational task. Automated rotation (via Vault PKI or a dedicated WireGuard controller) is a Phase 2 target. A compromised WireGuard key allows decryption of cross-cloud traffic, which includes Vault API calls from GCP workloads to the AWS Vault instance.

**Alert routing is not operational.** Falco generates events, but there's no pipeline from Falco output to a human right now. It's logging to stdout and that's it. The alert-router tool will close this gap, but until it's built, detection exists and response doesn't. This is the most operationally significant gap in the current stack.
