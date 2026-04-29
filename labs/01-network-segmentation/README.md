# Lab 01: Network Segmentation

This lab establishes the branch, HQ, and cloud zones used by the rest of
MERIDIAN LABS.

## Objective

Create a small topology that distinguishes:

- Branch A employee, guest, and local service zones
- Branch B employee, guest, and local service zones
- HQ admin, internal service, and telemetry zones
- Cloud public app and monitoring placeholders

## Current State

Flow table defined. The first real segmentation rules are intentionally left as
a hands-on learning task.

## Flow Table

See `flows.md` for the initial zone model, allowed flows, denied flows,
validation plan, assumptions, and local-lab limitations.

## Expected Evidence

When implemented, this lab should show:

- allowed employee-to-service traffic
- allowed branch-to-HQ application traffic
- blocked guest-to-employee traffic
- blocked guest-to-local-service traffic unless explicitly justified
- blocked branch-to-branch lateral traffic unless explicitly justified

See `LEARNING_TASK.md` for the implementation prompt.
