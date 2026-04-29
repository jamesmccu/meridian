# Lab 01 Flow Table

This document defines the first intended segmentation behavior for MERIDIAN
LABS. It is design intent only. No firewall, Docker network, VPN, or routing
implementation exists in this lab yet.

## Zones

| Zone | Initial Placeholder | Trust Level | Purpose |
|---|---|---|---|
| Branch employee client | `branch-employee-client` | trusted branch user | Represents a managed employee workstation or user workload. |
| Branch guest client | `branch-guest-client` | untrusted local user | Represents guest or BYOD traffic that must not reach internal branch services. |
| Branch local service | `branch-local-service` | restricted branch service | Represents a small office dependency such as a local file, print, or utility service. |
| HQ internal app | `hq-internal-app` | internal service | Represents an HQ-hosted business application reachable by approved branch users. |
| Telemetry placeholder | `hq-telemetry` | restricted infrastructure | Represents central log or event collection. |
| Cloud/public placeholder | `cloud-public-app` | external/public dependency | Represents a public app or cloud service dependency. |

Branch B is intentionally not implemented in the first flow table. The first
validated control path should prove the Branch A pattern before duplicating it.

## Allowed Flows

| ID | Source Zone | Destination Zone | Service | Reason | Initial Validation Idea |
|---|---|---|---|---|---|
| A1 | Branch employee client | Branch local service | HTTP or TCP health endpoint | Employees need approved access to a local branch service. | Employee client receives a successful response from the local service. |
| A2 | Branch employee client | HQ internal app | HTTP or TCP health endpoint | Employees need approved access to an HQ business service. | Employee client receives a successful response from the HQ placeholder. |
| A3 | Branch local service | Telemetry placeholder | log/event submission placeholder | Local service should be able to emit telemetry centrally. | Local service can send a single local test event or health payload. |
| A4 | HQ internal app | Cloud/public placeholder | HTTP health endpoint | HQ services may depend on an approved public/cloud endpoint. | HQ app receives a successful response from the cloud placeholder. |

## Denied Flows

| ID | Source Zone | Destination Zone | Expected Result | Reason | Initial Validation Idea |
|---|---|---|---|---|---|
| D1 | Branch guest client | Branch employee client | blocked or no route | Guest traffic must not reach employee systems. | Guest client cannot connect to an employee placeholder endpoint. |
| D2 | Branch guest client | Branch local service | blocked or no route | Guest traffic must not reach restricted branch services by default. | Guest client cannot connect to the local service endpoint. |
| D3 | Branch guest client | HQ internal app | blocked or no route | Guest traffic should not inherit branch employee trust. | Guest client cannot connect to the HQ app endpoint. |
| D4 | Branch employee client | Telemetry placeholder management surface | blocked or no route | Telemetry infrastructure management should not be exposed to branch clients. | Employee client cannot reach a management/admin placeholder port. |
| D5 | Branch local service | Branch employee client | blocked or no route | Local service compromise should not create a path back to employee systems. | Local service cannot initiate a connection to employee placeholder endpoint. |
| D6 | Branch A zones | Branch B zones | absent or blocked | Branch-to-branch lateral access should not exist in the first lab. | No Branch B network exists yet; later validation should show blocked transit. |

## Validation Plan

The first implementation should produce evidence for at least:

- A1: employee client reaches branch local service.
- A2: employee client reaches HQ internal app.
- D1: guest client cannot reach employee client.
- D2: guest client cannot reach branch local service.

Evidence should be recorded in a future `evidence.md` file with:

- command run
- expected result
- actual result
- conclusion
- limitation, if any

## Assumptions

- The first implementation will be local-only.
- Docker Compose networks are acceptable for the first topology unless a blocker
  appears.
- Service placeholders can be simple health endpoints.
- The first lab models reachability and segmentation intent, not production
  firewall feature parity.
- No real credentials, customer data, or external targets are used.

## Docker And Local-Lab Limitations

If Docker Compose is used for the first topology, document these limitations in
the evidence:

- Docker networks model local isolation, not a production branch firewall.
- Container DNS and bridge networking may behave differently from routed office
  networks.
- A blocked path in Docker proves the lab policy intent, not enterprise-grade
  enforcement.
- Host access must be reviewed separately; lab containers should not expose
  developer workstation services.

## Next Step

Implement the smallest local topology that can validate A1, A2, D1, and D2.
Start with one branch and one HQ placeholder before adding Branch B.
