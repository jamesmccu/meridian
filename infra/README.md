# Infrastructure

This directory is reserved for infrastructure automation.

Meridian separates infrastructure concerns by target:

- `ansible/` for homelab host bootstrap and Linux configuration.
- `opentofu/aws/` for AWS resources such as DNS, KMS, object storage, IAM, and
  managed security services.
- `opentofu/gcp/` for optional GCP experiments when there is a specific multi-cloud
  learning goal.

No deployable infrastructure modules are present yet.
