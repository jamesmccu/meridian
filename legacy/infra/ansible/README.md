# Ansible

This directory is reserved for homelab host bootstrap.

Expected future scope:

- Base Linux packages.
- User and SSH hardening.
- Kernel and sysctl settings.
- Container runtime setup.
- k3s installation prerequisites.
- Node exporter or host telemetry agents.
- auditd/osquery configuration.

Ansible should manage host state that is not naturally managed by Kubernetes.
