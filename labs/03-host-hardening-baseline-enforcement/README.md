# Host Hardening & Baseline Enforcement

## Problem

Branch and HQ systems often drift from secure defaults as services are added,
debug settings remain enabled, or management interfaces become too reachable.
This lab addresses the practical problem of defining a small baseline, applying
it consistently, and verifying that hosts remain within expected configuration.

## Scenario

In MERIDIAN LABS, branch service placeholders, HQ services, and telemetry
components need basic hardening before they become trusted parts of the lab. The
baseline should support segmentation and incident response without pretending to
be a full endpoint management platform.

## Security Objectives

- Define a small hardening baseline tied to the lab threat model.
- Reduce unnecessary service exposure.
- Separate administrative access from normal user paths.
- Create repeatable checks for expected host or service state.
- Document operational tradeoffs introduced by hardening.

## What This Lab Demonstrates

This lab demonstrates secure configuration management, baseline enforcement,
drift awareness, and the ability to explain why a control exists. It favors
manual understanding before automation.

## Real-World Implementations

This maps to control families and platforms such as:

- endpoint management systems
- configuration management tools
- secure baseline frameworks
- vulnerability management workflows
- drift detection systems
- privileged access workflows
- infrastructure-as-code workflows

## Learning Task

Do not solve the implementation from this README. Use `LEARNING_TASK.md` for the
hands-on prompt.

## Expected Outcome

A successful implementation should apply one narrow baseline to a lab host or
service placeholder and produce evidence that the intended control state exists
without breaking required service behavior.

## Validation

Validation should include:

- before and after state for one hardening control
- proof the expected service still works
- proof an unnecessary exposure is removed or blocked
- notes on controls deferred to later phases

## Reflection Questions

- Which hardening control most directly supports the threat model?
- What control would be different on a real workstation or server?
- What should be continuously monitored versus checked during deployment?
- Where does automation help, and where can it hide weak understanding?
