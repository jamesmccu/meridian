# Learning Task: Telemetry, Detection & Response

> Development note: this guided task is retained for implementation practice.
> It is not the platform architecture source of truth. Start from
> `observability/schemas/` and `detection-engineering/` for current contracts.

## Goal

Build the first local telemetry parser, correlator, or detection report for the
distributed office lab.

## Background

Telemetry should make control behavior visible. The first detection should be
safe, local, and tied to a specific branch/HQ abuse case such as denied guest
access, suspicious lateral movement, or unexpected service behavior.

## Constraints

- Must run locally where possible.
- Must not use real credentials.
- Must not scan or touch external targets.
- Must be safe and lab-contained.
- Prefer small working examples over large scaffolding.
- Do not add offensive tooling.
- Do not turn the telemetry stack into a general observability platform.

## Starter Hints

- Start with one denied-flow or suspicious-flow event from the segmentation lab.
- A local JSON file is acceptable before a full event pipeline.
- Reuse `tools/meridian-detect` when you are ready to write Python.
- Keep the first event schema explicit: source zone, destination zone, action,
  service, timestamp, and reason are enough.
- Write down false-positive assumptions early.

## Deliverables

- One sample local event source.
- A minimal parser, correlator, or report path.
- One documented detection idea tied to an abuse case.
- Validation evidence showing expected output.
- Notes on missing fields, false positives, and future enrichment.

## Validation Steps

- Generate or capture one safe local event.
- Run the parser, correlator, or report command.
- Confirm the output identifies the relevant zone, flow, and action.
- Confirm benign or unrelated events do not produce the same finding.

## Interview Notes

- Explain why the first detection was scoped to one abuse case.
- Describe which telemetry was required and which context was missing.
- Discuss how detection evidence feeds incident response.
- Be clear about what is local simulation versus production telemetry.
