# OpenTofu

This directory is reserved for cloud infrastructure modules.

OpenTofu/Terraform should be used for provider-native resources such as:

- DNS zones and records.
- Object storage for backups.
- KMS keys and aliases.
- IAM roles and policies.
- Managed security services.
- Optional cloud VMs for specific experiments.

Homelab host configuration belongs under `infra/ansible/`.
