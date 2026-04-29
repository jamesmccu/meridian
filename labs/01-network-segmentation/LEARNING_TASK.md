# Learning Task: Network Segmentation

## Goal

Implement the first real segmentation policy for the distributed office lab.

## Background

The core scenario has two branch offices, an HQ control plane, and cloud
placeholders. Each branch has employee, guest, and local service zones. The
security goal is to make allowed paths explicit and deny lateral paths by
default.

## Constraints

- Use local lab-owned containers or VMs only.
- Do not scan external targets.
- Keep the first version small enough to explain in a code review.
- Do not introduce a heavy firewall platform before simple local controls are
  understood.
- Document every allowed flow and why it exists.

## Expected Output

- A topology note or config showing the zones.
- A minimal segmentation policy.
- Validation evidence for at least two allowed flows and two denied flows.
- Notes about what the local implementation does not model accurately.

## Hints

- Start by writing the allowed flow table before writing rules.
- Treat guest networks as untrusted.
- Validate denied flows as deliberately as allowed flows.
- Prefer one working branch and HQ path before duplicating the pattern.

## Validation Steps

- From an employee zone, reach the approved local service.
- From an employee zone, reach the approved HQ service.
- From a guest zone, fail to reach an employee zone.
- From a guest zone, fail to reach a local service unless explicitly allowed.
- Record commands and results in the lab README or a short evidence file.

## Reflection Questions

- Which deny rule produced the most useful security boundary?
- Which flow was harder to model locally than expected?
- What would change if the branch used a real firewall appliance?
- What telemetry would help prove the segmentation is working over time?
