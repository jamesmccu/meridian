# Learning Task: Host Hardening & Baseline Enforcement

## Goal

Create the first baseline host or service hardening implementation for the lab.

## Background

Hardening reduces unnecessary exposure and makes privileged access deliberate.
The first baseline should be small enough to explain and validate before it is
wrapped in automation.

## Constraints

- Must run locally where possible.
- Must not use real credentials.
- Must not scan or touch external targets.
- Must be safe and lab-contained.
- Prefer small working examples over large scaffolding.
- Do not copy a generic benchmark wholesale.
- Do not write the first hardening playbook before the control is understood.

## Starter Hints

- Pick one or two controls tied directly to the threat model.
- Start with listening services, exposed ports, users, or permissions.
- Separate "required now" from "defer until later."
- Capture the before state before changing anything.
- Convert manual steps into automation only after validation is clear.

## Deliverables

- A short baseline note explaining selected controls.
- A first manual implementation against a lab host or service placeholder.
- Validation commands and results.
- Notes on deferred controls.

## Validation Steps

- Show before and after state for one control.
- Confirm required service behavior still works.
- Confirm unnecessary exposure is removed or blocked.
- Record the operational tradeoff created by the control.

## Interview Notes

- Explain why you chose a small baseline instead of a full benchmark.
- Tie the control back to segmentation, access, or incident response.
- Describe how you would scale the baseline after the first validated control.
- Be clear about what remains manual and what should become automated later.
