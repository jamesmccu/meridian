# MERIDIAN LABS Modules

The lab modules are ordered so each phase builds on the previous one. Each
module starts with documentation and a guided learning task before real
implementation is added.

| Module | Purpose | Current State |
|---|---|---|
| `01-network-segmentation` | Define zones, allowed flows, and blocked flows. | Guided task only. |
| `02-secure-connectivity` | Add authenticated branch-to-HQ connectivity. | Guided task only. |
| `03-host-hardening` | Establish baseline host and service controls. | Guided task only. |
| `04-telemetry-detection` | Preserve and extend v2 telemetry/detection work. | Guided task plus retained assets references. |
| `05-policy-as-code` | Add lightweight repository policy checks. | Guided task only. |

Do not add real credentials, external targets, or broad offensive tooling to
these modules. Any traffic generation or scanning must stay inside lab-owned
local containers or virtual machines.
