# AWS Infrastructure

This directory is reserved for AWS infrastructure managed by OpenTofu.

Recommended first resources:

- Route 53 records for selected public services.
- S3 bucket for backups.
- KMS key for encryption workflows and future Vault auto-unseal.
- IAM roles and policies for least-privilege access.
- GuardDuty and Security Hub enablement.
- IAM Access Analyzer.

AWS should be used where it teaches cloud-native security primitives rather than
duplicating services already running in the homelab.
