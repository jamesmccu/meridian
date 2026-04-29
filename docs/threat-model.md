# Threat Model

This threat model covers the MERIDIAN LABS distributed office scenario. It is a
starting point and should be refined after the first working topology exists.

## Assets

| Asset | Why It Matters |
|---|---|
| HQ internal app | Represents business service access from branches. |
| Identity-like service placeholder | Represents authentication and directory dependency without implementing a real IdP. |
| Admin workstation | Represents privileged operational access. |
| Branch local service | Represents local office dependencies that should not be exposed broadly. |
| Telemetry collector | Stores logs and detection data that support investigation. |
| Secure tunnel configuration | Controls branch-to-HQ trust and reachability. |
| Policy and automation files | Define intended state and should be reviewed before deployment. |

## Actors

| Actor | Description |
|---|---|
| Branch employee | Legitimate user on an employee subnet. |
| Guest user | Untrusted user on a guest subnet. |
| Administrator | Operator managing lab services and reviewing telemetry. |
| Compromised branch host | Employee or service host with attacker-controlled behavior. |
| External opportunistic actor | Internet-origin actor interacting only with exposed cloud/public placeholders. |
| Misconfigured automation | Non-malicious but risky change that weakens segmentation or logging. |

## Trust Boundaries

- guest subnet to employee subnet
- employee subnet to branch service subnet
- branch office to HQ
- administrator access path to management interfaces
- HQ services to cloud services
- lab workloads to the developer workstation running the lab

## Abuse Cases

| Abuse Case | Example Impact |
|---|---|
| Guest reaches employee subnet | Unauthorized access path from untrusted network. |
| Branch host reaches HQ management interface | Lateral movement into control-plane services. |
| Compromised branch service scans peer networks | Discovery and lateral movement risk inside the lab. |
| Tunnel allows all branch-to-branch traffic | Excessive trust between offices. |
| Telemetry collector is reachable from guest networks | Tampering, noise generation, or information exposure. |
| Automation permits broad inbound rules | Configuration drift becomes a security regression. |
| Logs omit denied or suspicious flows | Incident response lacks evidence. |

## Example Mitigations

- default-deny segmentation between guest, employee, service, HQ, and cloud zones
- explicit allow-list flows for required services
- authenticated and encrypted branch-to-HQ tunnel
- management interfaces bound to HQ admin paths only
- central telemetry collection with local, safe event generation
- CI checks that reject obviously unsafe config patterns
- documented validation steps for each lab module

## Assumptions

- The lab runs on a trusted local development machine.
- Early phases use placeholders for identity, cloud, and business services.
- No real credentials, customer data, or external targets are used.
- Network scanning, if added, is limited to lab-owned local containers or VMs.
- The first implementation optimizes for learning value and explainability, not
  production parity.

## Limitations

- This is not a full enterprise architecture.
- Container networking may not reproduce every firewall, VPN, or endpoint
  behavior found in production networks.
- The identity-like service is a placeholder until a later phase justifies a real
  implementation.
- The initial threat model is design-time only and must be updated after working
  traffic flows and telemetry exist.
