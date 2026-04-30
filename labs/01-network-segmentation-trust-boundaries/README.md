# Network Segmentation & Trust Boundaries

## Problem

Small offices often grow faster than their network controls. Employee devices,
guest devices, local services, HQ applications, and telemetry systems can become
reachable through overly broad paths. This lab addresses the practical problem
of defining zones, limiting traffic to approved flows, and preventing lateral
movement from untrusted or compromised systems.

## Scenario

In MERIDIAN LABS, a branch office connects to HQ and selected cloud services.
The first segmentation model focuses on one branch, an HQ internal application,
a telemetry placeholder, and a cloud/public placeholder. Branch B is deferred
until the Branch A pattern is validated.

## Security Objectives

- Define branch, HQ, telemetry, and cloud/public zones.
- Allow only documented employee-to-service and employee-to-HQ paths.
- Block guest access to employee, local service, and HQ internal paths.
- Prevent local service compromise from creating a path back to employee systems.
- Preserve a clear validation path for allowed and denied traffic.

## What This Lab Demonstrates

This lab demonstrates how to convert architecture intent into testable
segmentation behavior. It emphasizes trust boundaries, traffic allow lists,
default-deny thinking, lateral movement prevention, and evidence-based
validation before expanding the topology.

## Real-World Implementations

This maps to control families and platforms such as:

- zone-based firewalls
- VLANs and routed segmentation
- secure web gateways
- SASE / SSE platforms
- network access control systems
- network detection and response platforms
- infrastructure-as-code workflows for network policy

## Learning Task

Do not solve the implementation from this README. Use `LEARNING_TASK.md` for the
hands-on prompt and `flows.md` for the current design intent.

## Expected Outcome

A successful implementation should produce a small local topology with documented
allowed and denied paths. At minimum, the employee client should reach the
approved branch local service and HQ placeholder, while the guest client should
fail to reach internal branch service paths.

## Validation

Validation should include command output or evidence showing:

- an approved employee-to-local-service path succeeds
- an approved employee-to-HQ path succeeds
- a guest-to-employee path fails
- a guest-to-local-service path fails
- limitations of the local model are documented

## Reflection Questions

- Which traffic path deserves the most scrutiny before it is allowed?
- What boundary prevents guest access from becoming internal access?
- What does the local lab prove, and what would still need production-grade
  validation?
- How would telemetry confirm segmentation is still working over time?
- What would change if the branch had intermittent connectivity to HQ?
