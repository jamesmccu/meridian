# Telemetry, Detection & Response

## Problem

Security controls are difficult to trust if they do not produce useful evidence.
Branches, HQ services, and control-plane components need telemetry that supports
alerting, investigation, and response without collecting unnecessary data or
turning the lab into a generic observability platform.

## Scenario

In MERIDIAN LABS, telemetry should help answer questions such as whether guest
traffic attempted to reach internal services, whether branch-to-HQ access is
being used as intended, and whether a local service behaved unexpectedly.

## Security Objectives

- Collect safe, local lab telemetry from branch and HQ placeholders.
- Preserve useful event-pipeline work from MERIDIAN v2.
- Build one small detection, parser, correlator, or report.
- Connect findings to abuse cases from the threat model.
- Document limitations, false positives, and missing context.

## What This Lab Demonstrates

This lab demonstrates security telemetry design, local event generation, event
normalization, detection thinking, investigation workflow, and response
readiness. It keeps the first detection small and tied to a specific abuse case.

## Real-World Implementations

This maps to control families and platforms such as:

- network detection and response platforms
- log ingestion pipelines
- endpoint detection and response platforms
- SIEM and security data platforms
- alerting and case-management workflows
- incident response runbooks
- safe local simulation environments

## Learning Task

Do not solve the implementation from this README. Use `LEARNING_TASK.md` for the
hands-on prompt.

## Expected Outcome

A successful implementation should produce one safe local event source, route or
parse the event, and generate a small detection output or report tied to a lab
abuse case.

## Validation

Validation should include:

- one generated or captured local event
- parser, correlator, or report output
- confirmation that expected fields are present
- confirmation that benign or unrelated events do not produce the same finding

## Reflection Questions

- Which event field mattered most for the detection?
- What context was missing during investigation?
- Would the detection help during a real branch incident?
- What belongs in branch-local telemetry versus central telemetry?
- What false positives would need tuning before production use?

## Retained MERIDIAN v2 Assets

The following existing assets are preserved for this lab:

- `observability/quickwit/quickwit.yaml`
- `observability/otel/vector.yaml`
- `observability/otel/fluent-bit.conf`
- `observability/victoriametrics/prometheus.yml`
- `tools/meridian-detect/`
- `security/trivy/`

These files remain in their current locations so existing checks and tooling do
not break during the lab reframing.
