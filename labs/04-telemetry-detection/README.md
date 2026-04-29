# Lab 04: Telemetry And Detection

This lab is the future home for the useful MERIDIAN v2 detection and telemetry
work.

## Objective

Collect local lab telemetry and build a small detection or report that supports
investigation of the distributed office scenario.

## Retained v2 Assets

The following existing assets are preserved for this lab:

- `observability/quickwit/quickwit.yaml`
- `observability/otel/vector.yaml`
- `observability/otel/fluent-bit.conf`
- `observability/victoriametrics/prometheus.yml`
- `tools/meridian-detect/`
- `security/trivy/`

These files remain in their current locations so existing checks and tooling do
not break during the repositioning.

## Current State

Scaffold plus retained assets. The first real parser, correlator, or detection
logic is intentionally left as a hands-on learning task.

## Expected Evidence

When implemented, this lab should show:

- a safe local event source
- event routing into a local collector or file
- a small parser, correlator, or detection report
- documented false-positive and limitation notes

See `LEARNING_TASK.md` for the implementation prompt.
