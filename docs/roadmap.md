# Roadmap

MERIDIAN LABS should progress in phases. Each phase should produce a small,
reviewable artifact with validation evidence before the next phase grows the
implementation.

## Phase 1: Topology And Segmentation

Goal: define the lab topology, zones, allowed flows, and blocked flows.

Expected outcomes:

- branch A, branch B, HQ, and cloud placeholders
- employee, guest, service, admin, telemetry, and public zones
- first manual segmentation policy
- documented validation of allowed and denied paths

Owner learning work:

- first real firewall or segmentation rules
- first topology diagram after the traffic model is understood

## Phase 2: VPN / Secure Connectivity

Goal: connect branch offices to HQ through an authenticated and encrypted path.

Expected outcomes:

- branch-to-HQ tunnel design
- explicit routes and allowed services
- failure-mode notes for tunnel down or misrouted traffic
- validation that guest and branch-to-branch lateral paths remain restricted

Owner learning work:

- first VPN or secure connectivity implementation

## Phase 3: Host Hardening

Goal: apply baseline hardening to lab hosts or service containers without hiding
the controls behind too much automation.

Expected outcomes:

- minimal hardening baseline
- documented control rationale
- repeatable validation steps
- first Ansible playbook after manual understanding exists

Owner learning work:

- first Ansible hardening playbook

## Phase 4: Telemetry And Detection

Goal: collect useful local telemetry and produce a small detection or report.

Expected outcomes:

- branch and HQ log flow into a collector
- safe local traffic simulation
- retained v2 assets mapped into this module
- first Python parser or correlator
- documented detection limitations

Owner learning work:

- first Python log parser/correlator

## Phase 5: Policy-As-Code / CI Checks

Goal: add lightweight checks that prevent unsafe lab configuration changes.

Expected outcomes:

- repository-local policy checks
- CI feedback for configuration hygiene
- clear examples of accepted and rejected changes
- no heavyweight policy platform unless justified by the lab

Owner learning work:

- first GitHub Actions policy check

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
