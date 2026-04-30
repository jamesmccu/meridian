# Learning Task: Secure Connectivity & Remote Access

## Goal

Implement the first secure branch-to-HQ connectivity path without weakening the
segmentation model.

## Background

Secure connectivity should provide authenticated and encrypted access to
approved services. It should not create broad implicit trust between all branch,
HQ, guest, and management zones.

## Constraints

- Must run locally where possible.
- Must not use real credentials.
- Must not scan or touch external targets.
- Must be safe and lab-contained.
- Prefer small working examples over large scaffolding.
- Do not implement broad branch-to-branch transit unless you can justify it.

## Starter Hints

- Choose one branch first.
- Keep the tunnel endpoint separate from the protected service in your notes.
- Make routes and allowed services explicit.
- Think through what should happen when the secure path is unavailable.
- Preserve logs or simple evidence for later telemetry work.

## Deliverables

- A short design note for the selected connectivity approach.
- Minimal local configuration for one branch-to-HQ path.
- Validation evidence for approved access.
- Validation evidence for blocked guest or lateral access.
- A short failure-mode note.

## Validation Steps

- Confirm branch employee access to the approved HQ service.
- Confirm branch guest access to HQ internal or management paths fails.
- Confirm no unintended branch-to-branch transit exists.
- Disable the secure path and record the observed failure behavior.

## Interview Notes

- Explain the difference between encrypted transport and authorized access.
- Describe how the tunnel scope was limited.
- Discuss how remote access decisions could include identity, device posture, or
  role.
- Identify the rule or route that would be most dangerous if broadened.
