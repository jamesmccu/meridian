# Validation

This directory records validation expectations for shared MERIDIAN LABS platform
contracts.

Current validation is limited to existing repository checks:

- Python tests, linting, and type checking for `tools/meridian-detect`.
- YAML parsing for repository manifests.
- Docker Compose config validation for `onprem/docker-compose.yml`.
- Trivy filesystem and configuration scanning when Trivy is installed.

Future validation should add small, explicit checks for:

- topology contract syntax
- service catalog consistency
- network catalog consistency
- allowed and denied segmentation flows
- telemetry event schema compliance

Validation evidence should include the command, expected result, actual result,
and limitation.
