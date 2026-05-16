# Secure Connectivity & Remote Access

> Platform note: this file is retained as guided-lab context. Future
> architecture-driven connectivity contracts belong in
> `network-security/connectivity/`.

## Problem

Branch offices need reliable access to HQ services without turning the network
into a flat trust domain. Remote access and branch connectivity must be
authenticated, encrypted, observable, and limited to approved resources.

## Scenario

In MERIDIAN LABS, branch offices connect to HQ services over a trusted path. The
connectivity model should preserve the segmentation decisions from Lab 01 and
avoid accidental branch-to-branch or guest-to-HQ access.

## Security Objectives

- Define an authenticated and encrypted branch-to-HQ path.
- Keep guest traffic outside the trusted connectivity path.
- Limit remote access to approved services and administrative paths.
- Document failure behavior when the secure path is unavailable.
- Preserve visibility into tunnel or remote-access use.

## What This Lab Demonstrates

This lab demonstrates how secure connectivity design affects trust boundaries.
It focuses on routes, tunnel scope, service exposure, remote access boundaries,
and the operational evidence needed to show that secure access did not become
broad network access.

## Real-World Implementations

This maps to control families and platforms such as:

- site-to-site VPNs
- client VPNs and remote access gateways
- SASE / SSE platforms
- identity-aware access proxies
- bastion and privileged access workflows
- secure web gateways
- network telemetry and access logs

## Learning Task

Do not solve the implementation from this README. Use `LEARNING_TASK.md` for the
hands-on prompt.

## Expected Outcome

A successful implementation should show an approved branch-to-HQ path that works
for intended traffic while guest, lateral, and management access remain blocked
unless explicitly justified.

## Validation

Validation should include evidence showing:

- approved branch employee access to an HQ service works
- guest access to HQ internal or management paths fails
- branch-to-branch transit is absent or blocked
- tunnel-down behavior is documented

## Reflection Questions

- What trust did the secure connectivity path create?
- Which traffic should never inherit tunnel access?
- How would identity or device posture change the access decision?
- What telemetry would show misuse or misconfiguration?
- What is the smallest secure path that satisfies the business need?
