# Learning Task: Host Hardening

## Goal

Create the first baseline host or service hardening implementation.

## Background

Hardening should reduce exposed services, tighten defaults, and make privileged
access deliberate. In this lab, the point is to understand the controls before
wrapping them in automation.

## Constraints

- Start with a very small baseline.
- Do not copy a generic benchmark wholesale.
- Do not add secrets or real credentials.
- Do not make Ansible hide controls you cannot explain manually.
- Keep any automation local and reviewable.

## Expected Output

- A short baseline describing the selected controls.
- A first implementation, preferably against a lab host or service placeholder.
- Validation commands that prove the control state.
- Notes about controls deferred to later phases.

## Hints

- Pick controls tied to the lab threat model.
- Check listening services and management paths first.
- Separate "must have now" from "good later."
- Convert manual steps into Ansible only after the baseline is clear.

## Validation Steps

- Show the before and after state for one hardening control.
- Confirm the expected service still works.
- Confirm an unnecessary exposure is removed or blocked.
- Record any operational tradeoff caused by the control.

## Reflection Questions

- Which hardening control directly supports segmentation or incident response?
- Which control would be different on a real workstation or server?
- What should be measured continuously versus checked during deployment?
- What would make this baseline too broad for a small branch office?
