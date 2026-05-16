# MERIDIAN LABS Modules

> Platform note: `labs/` is retained as legacy/current guided-lab content during
> the MERIDIAN LABS reframe. Architecture-driven platform contracts now belong
> in top-level domains such as `core-platform/`, `network-security/`,
> `detection-engineering/`, and `incident-response/`.

The lab modules are organized around real security engineering problems in a
distributed office environment. Each module starts with a README and guided
learning task before implementation is added.

| Module | Problem Area | Current State |
|---|---|---|
| `01-network-segmentation-trust-boundaries` | Network segmentation, trust boundaries, least-privilege traffic, and lateral movement prevention. | Flow table and guided task. |
| `02-secure-connectivity-remote-access` | Encrypted branch-to-HQ connectivity, remote access, and identity-aware access concepts. | Guided task only. |
| `03-host-hardening-baseline-enforcement` | OS hardening, secure configuration, drift detection, and fleet baseline management. | Guided task only. |
| `04-telemetry-detection-response` | Log ingestion, security telemetry, alerting, investigation workflows, and safe local simulation. | Guided task plus retained assets references. |
| `05-policy-as-code-automated-validation` | Config validation, CI/CD checks, infrastructure guardrails, and safe deployment workflows. | Guided task only. |

Do not add real credentials, external targets, or broad offensive tooling to
these modules. Any traffic generation or scanning must stay inside lab-owned
local containers or virtual machines.
