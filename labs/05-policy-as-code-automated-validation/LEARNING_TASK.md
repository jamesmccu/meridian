# Learning Task: Policy as Code & Automated Validation

> Development note: this guided task is retained for implementation practice.
> It is not the platform architecture source of truth. Shared validation
> direction starts in `core-platform/validation/`.

## Goal

Implement the first lightweight policy check for MERIDIAN LABS.

## Background

Automated validation should catch unsafe or inconsistent lab changes before they
are merged. The first rule should be narrow enough to understand in a pull
request and tied to a specific abuse case or design constraint.

## Constraints

- Must run locally where possible.
- Must not use real credentials.
- Must not scan or touch external targets.
- Must be safe and lab-contained.
- Prefer small working examples over large scaffolding.
- Do not introduce a heavyweight policy platform unless the first rule needs it.
- Keep validation output readable.

## Starter Hints

- Look for unsafe broad access patterns in future topology or policy files.
- A small script can be better than adopting a full policy engine too early.
- Make the error message teach the intended design.
- Tie the rule to the threat model.
- Keep accepted and rejected examples small.

## Deliverables

- One policy rule.
- A local command or CI workflow that runs it.
- One passing example.
- One failing example or documented failure mode.
- A short explanation of what the rule cannot prove.

## Validation Steps

- Run the policy check against a passing config.
- Run the policy check against a deliberately unsafe local example.
- Confirm the failure message identifies the risky pattern.
- Confirm the rule is documented in the lab README or evidence notes.

## Interview Notes

- Explain why the first rule was narrow.
- Describe how CI becomes a security review control.
- Discuss what the policy cannot prove.
- Identify when exceptions should be documented instead of silently bypassed.
