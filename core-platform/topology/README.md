# Topology

This directory defines the initial MERIDIAN LABS local enterprise topology
contract. The contract describes intended zones, sites, services, and traffic
relationships before implementation details are expanded.

`local-enterprise.yaml` is design intent. It should be used by later validation
and implementation work, but it does not currently provision infrastructure.

## Principles

- Model one branch and one HQ control-plane path before adding scale.
- Keep cloud and identity dependencies explicit, even when represented by local
  placeholders.
- Keep management access separate from employee and guest paths.
- Capture implementation gaps as limitations instead of implying controls exist.
