# Security Policy

Meridian is a public portfolio and homelab platform repository. It should not
contain production secrets, private infrastructure inventories, real provider
account identifiers, private keys, generated certificates, Terraform state,
kubeconfigs, Vault tokens, or Datadog/API tokens.

## Reporting Issues

For security issues in this repository, open a private security advisory on
GitHub if available. If that is not available, contact the repository owner
through the public contact links in the profile.

Do not open a public issue containing secrets, exploit details, private hostnames,
or credentials.

## Public Repository Rules

- Commit templates and examples, not live secrets.
- Keep generated certificates and private keys out of Git.
- Keep local runtime data out of Git.
- Keep provider account IDs, public IP inventories, and private network diagrams
  out of public docs unless they are intentionally sanitized.
- Use placeholders such as `example.com`, `10.0.0.0/24`, or `<account-id>` for
  documentation examples.
- Store deploy-time secrets in Vault, GitHub Actions secrets, SOPS, or another
  documented secret-management path.

## Current Scope

The repository currently contains local lab configuration, CI workflows, security
scanner configuration, design documentation, and scaffolding for future GitOps/IaC
work. It is not a certified compliance implementation or a production deployment.
