# Learning Task: Policy-As-Code

## Goal

Implement the first lightweight policy check for MERIDIAN LABS.

## Background

Policy-as-code should catch unsafe or inconsistent lab changes before they are
merged. The first rule should be narrow enough to understand in a pull request.

## Constraints

- Start with one rule.
- Do not introduce a heavyweight policy platform unless the rule needs it.
- Do not block broad classes of changes without a clear reason.
- Keep CI feedback readable.
- Avoid external services or paid dependencies.

## Expected Output

- One policy rule.
- A local command or GitHub Actions workflow that runs it.
- One passing example.
- One failing example or documented failure mode.
- A short explanation of what the rule cannot prove.

## Hints

- Look for unsafe broad access patterns in future topology or policy files.
- A small script can be better than adopting a full policy engine too early.
- Make the error message teach the intended design.
- Keep the rule tied to the threat model.

## Validation Steps

- Run the policy check against a passing config.
- Run the policy check against a deliberately unsafe local example.
- Confirm the failure message identifies the risky pattern.
- Confirm the rule is documented in the lab README.

## Reflection Questions

- What risk does this rule reduce?
- What unsafe change would still bypass it?
- Would the rule be noisy in normal development?
- When would a real policy engine become justified?
