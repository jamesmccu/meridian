# Learning Task: Network Segmentation & Trust Boundaries

## Goal

Implement the first local segmentation control path for the distributed office
lab.

## Background

Segmentation is a practical way to reduce blast radius. The goal is to define
which zones can communicate, make denied paths explicit, and validate behavior
with evidence instead of assuming the design works.

## Constraints

- Must run locally where possible.
- Must not use real credentials.
- Must not scan or touch external targets.
- Must be safe and lab-contained.
- Prefer small working examples over large scaffolding.
- Do not introduce a heavy firewall platform before simple local controls are
  understood.

## Starter Hints

- Start with the allowed and denied flows in `flows.md`.
- Validate one branch before duplicating the pattern.
- Use simple service placeholders; application behavior is not the point.
- Treat guest traffic as untrusted by default.
- Record denied-path evidence as carefully as successful-path evidence.

## Deliverables

- A minimal local topology or configuration.
- A documented segmentation policy.
- Validation evidence for at least two allowed flows and two denied flows.
- Notes on what the local implementation does not model accurately.

## Validation Steps

- Confirm the branch employee client can reach the approved branch local service.
- Confirm the branch employee client can reach the approved HQ placeholder.
- Confirm the branch guest client cannot reach the employee path.
- Confirm the branch guest client cannot reach the branch local service.
- Record commands, expected results, actual results, and conclusions.

## Interview Notes

- Explain why the first implementation started with one branch.
- Describe how least-privilege traffic rules reduced lateral movement risk.
- Be clear about what Docker or local networking can and cannot prove.
- Describe how this control would map to a production network boundary.
