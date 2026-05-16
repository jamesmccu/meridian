# Detection Engineering

`detection-engineering/` contains detection content, sample events, report
contracts, and scenario-specific validation material.

The existing Python CLI remains in `tools/meridian-detect/` for compatibility.
Future detection workflows should connect this module's sample events and
detection contracts to that tooling.

## Current Scope

- Sample-event scaffold.
- Detection documentation scaffold.
- Report documentation scaffold.

## Planned Scope

- Detection metadata.
- Event fixtures.
- Validation tests.
- Enrichment logic.
- Investigation and report outputs.

## Not Implemented Yet

- Production detection rules.
- SIEM deployment.
- Automated event ingestion from segmentation evidence.
