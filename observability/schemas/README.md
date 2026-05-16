# Observability Schemas

This directory defines event schema contracts for MERIDIAN LABS telemetry.

The current schema is an initial contract for local simulation events. It is
intended to support segmentation evidence, detection engineering fixtures, and
incident-response scenarios before a full ingestion pipeline is implemented.

## Current Schema

- `meridian-event.schema.json`: initial JSON Schema for security-relevant lab
  events.

## Notes

- Schema fields should stay small until a validated use case needs more context.
- Events must be safe and local to lab-owned containers, files, or simulations.
- Schema changes should account for detection fixtures in
  `detection-engineering/sample-events/`.
