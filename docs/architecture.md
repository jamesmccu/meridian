# MERIDIAN LABS Architecture

MERIDIAN LABS models a distributed office environment where small branch offices
connect to HQ services and selected cloud services. The architecture is designed
for hands-on security engineering practice: segmentation, secure connectivity,
configuration automation, telemetry, detection, and documentation.

## System Overview

```text
                 Cloud Zone
          public app placeholder
          monitoring placeholder
                    ^
                    |
                    v
HQ / Main Office Control Plane
  admin workstation
  identity-like service placeholder
  internal app
  telemetry collector
        ^                         ^
        | secure tunnel            | secure tunnel
        v                         v
 Branch Office A              Branch Office B
  employee subnet              employee subnet
  guest subnet                 guest subnet
  local service                local service
```

The first implementation should stay local-first. Docker networks, lightweight
containers, and simple scripts are acceptable for early validation. More complex
virtual networking, Ansible, or cloud resources should be introduced only when
they support a specific lab objective.

## Trust Boundaries

| Boundary | Why It Matters |
|---|---|
| Guest to employee subnet | Guest devices should not reach employee systems or local services unless explicitly allowed. |
| Branch to HQ | Branch traffic should be authenticated, encrypted, and limited to required services. |
| Admin workstation to infrastructure | Administrative access should be separate from normal user traffic. |
| Internal app to telemetry collector | Application and system logs should be routed without exposing the collector broadly. |
| HQ to cloud | Cloud-facing traffic should be explicit, observable, and constrained. |
| Lab host to lab network | Local host credentials and services must not be exposed to lab workloads. |

## Zones

| Zone | Example Contents | Security Intent |
|---|---|---|
| Branch employee | user workstation container or VM placeholder | Normal trusted user access to approved local, HQ, and cloud services. |
| Branch guest | guest client placeholder | Internet or public-app access only; no lateral movement into employee or service zones. |
| Branch service | print/file/local service placeholder | Minimal inbound access from employee subnet and controlled outbound access. |
| HQ admin | admin workstation placeholder | Administrative path for managing lab services and reviewing telemetry. |
| HQ services | identity-like service, internal app, telemetry collector | Central services reachable over explicit branch tunnels. |
| Cloud | public app and monitoring placeholders | External service dependency with controlled access and observable flows. |

## Data Flows

Initial flows to model:

- employee client to local branch service
- employee client to HQ internal app over secure connectivity
- branch telemetry to HQ collector
- admin workstation to infrastructure management endpoints
- HQ service to cloud monitoring placeholder
- guest client to public app only

Flows that should be blocked or called out as exceptions:

- guest client to employee subnet
- guest client to local branch service
- branch client to telemetry collector management interface
- branch-to-branch lateral access without an approved path
- direct access from lab workloads to host-only services

## Control Plane Versus Branch Offices

The HQ environment acts as the control plane for the lab. It hosts the admin
workstation, identity-like placeholder, internal application, and telemetry
collector. Branch offices should remain limited execution environments with
local service placeholders and secure connectivity back to HQ.

This separation supports realistic design questions:

- Which controls belong centrally at HQ?
- Which controls must remain local to a branch when connectivity is degraded?
- Which logs are generated locally but analyzed centrally?
- Which management interfaces should never be reachable from guest or employee
  subnets?

## Likely Technologies

Use the smallest tool that demonstrates the control clearly:

| Need | Likely Technology | Notes |
|---|---|---|
| Local topology | Docker Compose networks or lightweight VMs | Start with Docker where possible; use VMs only when kernel/network behavior requires it. |
| Secure tunnel | WireGuard, Tailscale-like model, or SSH tunnel placeholder | The first real implementation is intentionally left as a learning task. |
| Host hardening | Ansible | Introduce after the baseline hosts/services are defined. |
| Telemetry | Vector, Fluent Bit, Quickwit, `meridian-detect` | Existing v2 assets are retained here. |
| Security scanning | Trivy | Already present for repository/config/image checks. |
| CI checks | GitHub Actions | Keep checks lightweight and local to repository artifacts. |
| Diagrams | Mermaid, draw.io, or exported image | The first architecture diagram is left as a manual learning task. |

## Security Controls

MERIDIAN LABS should demonstrate controls in layers:

- segmentation policy between zones and subnets
- explicit allow-list traffic flows
- authenticated and encrypted branch-to-HQ connectivity
- least-privilege administrative access
- baseline host hardening
- central telemetry collection
- local detection and enrichment
- CI checks for configuration drift and unsafe patterns
- runbooks for investigation and response

Controls should be documented with the reason they exist, the expected behavior,
and the validation method. The lab should prefer one working example per phase
over broad scaffolding with no evidence.
