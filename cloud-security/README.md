# Cloud Security

`cloud-security/` is the planned home for cloud security baseline scenarios.

This directory is an initial scaffold. No cloud accounts, Terraform state, live
provider identifiers, or production cloud resources are stored here.

## Planned Scope

- AWS/cloud baseline contracts.
- Identity and access guardrails.
- Logging and monitoring baseline.
- Network baseline and public exposure controls.
- Policy validation for cloud configuration.

## Boundary

Cloud scenarios should remain provider-aware where useful but not certification
branded. Any real cloud implementation must avoid committing account-specific
identifiers, secrets, state files, or live credentials.
