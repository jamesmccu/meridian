# Roadmap

MERIDIAN LABS should progress in phases. Each phase should produce a small,
reviewable artifact with validation evidence before the next phase grows the
implementation.

## Phase 1: Network Segmentation And Trust Boundaries

Goal: define zones, least-privilege traffic paths, denied paths, and the first
validated segmentation behavior.

Expected outcomes:

- branch, HQ, telemetry, and cloud/public zones
- allowed and denied flow tables
- first manual segmentation implementation
- documented validation of allowed and denied paths
- limitations of the local model stated plainly

Owner learning work:

- first real firewall or segmentation rules
- first topology diagram after the traffic model is understood

## Phase 2: Secure Connectivity And Remote Access

Goal: connect branch offices to HQ through an authenticated, encrypted, and
scoped access path.

Expected outcomes:

- branch-to-HQ connectivity design
- explicit routes and allowed services
- guest and management access boundaries
- failure-mode notes for unavailable or misrouted connectivity
- validation that lateral paths remain restricted

Owner learning work:

- first VPN or secure connectivity implementation

## Phase 3: Host Hardening And Baseline Enforcement

Goal: apply a narrow hardening baseline to lab hosts or service placeholders and
verify expected state.

Expected outcomes:

- minimal hardening baseline tied to the threat model
- documented control rationale
- repeatable validation steps
- before/after evidence for at least one control
- first automation only after manual understanding exists

Owner learning work:

- first host hardening playbook

## Phase 4: Telemetry, Detection, And Response

Goal: collect useful local telemetry and produce a small detection, correlation,
or investigation output.

Expected outcomes:

- branch and HQ event flow into a local file, collector, or parser
- safe local traffic simulation
- retained v2 assets mapped into this module
- first parser, correlator, or report
- documented limitations and false-positive notes

Owner learning work:

- first Python log parser/correlator

## Phase 5: Policy As Code And Automated Validation

Goal: add lightweight validation that catches unsafe lab configuration changes
before they merge.

Expected outcomes:

- one repository-local policy check
- clear pass and fail examples
- readable local or CI feedback
- documented limits of the policy
- no heavyweight policy platform unless justified by the lab

Owner learning work:

- first CI/CD policy validation workflow

## Phase 6: Incident-Response Scenarios

Goal: create small investigation exercises once segmentation, telemetry, and
detection are working.

Expected outcomes:

- safe local incident scenarios
- expected telemetry and investigation path
- response notes or runbook entries
- lessons learned folded back into the threat model

Owner learning work:

- first threat-model refinement based on observed lab behavior
