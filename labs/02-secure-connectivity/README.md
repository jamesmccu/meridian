# Lab 02: Secure Connectivity

This lab adds an authenticated and encrypted branch-to-HQ path after the basic
zones and segmentation model exist.

## Objective

Model how Branch Office A and Branch Office B reach HQ services without opening
unnecessary branch-to-branch or guest-to-HQ paths.

## Current State

Scaffold only. The first real tunnel or secure connectivity implementation is
intentionally left as a hands-on learning task.

## Expected Evidence

When implemented, this lab should show:

- authenticated branch-to-HQ connectivity
- explicit routes or service access rules
- blocked guest access to HQ management surfaces
- blocked branch-to-branch lateral paths unless explicitly approved
- documented failure behavior when the secure path is unavailable

See `LEARNING_TASK.md` for the implementation prompt.
