# Learning Task: Secure Connectivity

## Goal

Implement the first secure branch-to-HQ connectivity path.

## Background

Branch offices should reach selected HQ services over a trusted path. The tunnel
or secure transport should not become a broad flat network that bypasses the
segmentation work from Lab 01.

## Constraints

- Use lab-owned local containers or VMs only.
- Do not use real production VPN credentials or provider accounts.
- Keep routes and allowed services explicit.
- Do not allow guest zones to inherit branch employee trust.
- Do not implement branch-to-branch access unless you can justify it.

## Expected Output

- A short design note explaining the chosen secure connectivity approach.
- Minimal configuration for one branch-to-HQ path.
- Validation evidence that approved traffic works through the path.
- Validation evidence that unapproved traffic remains blocked.

## Hints

- Choose one branch first.
- Make the tunnel endpoint and the protected service distinct in your notes.
- Think about what happens when the tunnel is down.
- Log or record connection attempts so the later telemetry lab has useful input.

## Validation Steps

- Confirm the branch employee zone can reach the approved HQ service.
- Confirm the branch guest zone cannot reach HQ management interfaces.
- Confirm another branch cannot use the tunnel as an unintended transit path.
- Stop or disable the secure path and record the observed failure mode.

## Reflection Questions

- What trust did the tunnel create?
- What trust did it avoid creating?
- Which route or rule would be most dangerous if broadened accidentally?
- What telemetry would indicate tunnel misuse?
