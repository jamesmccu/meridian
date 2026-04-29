# Learning Task: Telemetry And Detection

## Goal

Build the first local telemetry parser, correlator, or detection report for the
distributed office lab.

## Background

MERIDIAN v2 already contains useful telemetry and detection scaffolding. This
lab should reuse that work without forcing a Kubernetes-only architecture. The
first detection should be safe, local, and tied to the branch/HQ threat model.

## Constraints

- Use local lab-owned logs or generated events only.
- Do not ingest real personal, customer, or production data.
- Do not add offensive tooling.
- Keep the first parser or correlator small.
- Do not turn the telemetry stack into a general observability platform.

## Expected Output

- A sample local event source.
- A minimal parser, correlator, or report path.
- One documented detection idea tied to an abuse case.
- Validation evidence showing expected output.
- Notes about missing fields, false positives, and future enrichment.

## Hints

- Start with one denied-flow or suspicious-flow event from the segmentation lab.
- Reuse `tools/meridian-detect` when you are ready to write Python.
- Keep event fields boring and explicit: source zone, destination zone, action,
  service, timestamp, and reason are enough for the first pass.
- A local JSON file is acceptable before a full event pipeline.

## Validation Steps

- Generate or capture one safe local event.
- Run the parser or correlator.
- Confirm the output identifies the relevant zone, flow, and action.
- Confirm benign or unrelated events do not produce the same finding.

## Reflection Questions

- Which event field mattered most for the detection?
- What context was missing?
- Would this detection help during an actual branch incident?
- What should be enriched centrally versus at the branch?
