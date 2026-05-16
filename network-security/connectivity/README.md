# Connectivity

This module will define secure branch-to-HQ connectivity for MERIDIAN LABS.

The current state is an initial scaffold. Existing guided connectivity notes
remain in `labs/02-secure-connectivity-remote-access/` until a platform contract
and implementation are ready.

## Planned Scope

- Authenticated and encrypted branch-to-HQ path.
- Explicit route and service allow lists.
- Guest and management access boundaries.
- Failure-mode evidence when the secure path is unavailable.

## Not Implemented Yet

- VPN, WireGuard, SSH tunnel, or equivalent connectivity implementation.
- Automated route validation.
- Branch-to-branch transit controls.
