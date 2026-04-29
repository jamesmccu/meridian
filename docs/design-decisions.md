# Design Decisions

This document records the repo audit and the main decisions behind the pivot from
MERIDIAN v2 to MERIDIAN LABS.

## Current Repo Audit

The repository currently contains useful building blocks from the Kubernetes
runtime detection positioning:

| Area | Current Contents | MERIDIAN LABS Treatment |
|---|---|---|
| Root docs | README, changelog, structure, release notes, security policy | Rewrite positioning while keeping public hygiene guidance. |
| `docs/` | v2 architecture, learning map, runbook placeholder | Replace architecture with distributed office model and add threat model, roadmap, positioning, and decisions. |
| `observability/` | Quickwit, Vector, Fluent Bit, VictoriaMetrics config | Preserve as future telemetry/detection lab material. |
| `onprem/` | Docker Compose, Vault, Nginx, Node Exporter config | Preserve as reference material; do not expand until a lab needs it. |
| `security/` | Trivy docs and config | Preserve as repository hygiene and future policy-as-code input. |
| `tools/meridian-detect/` | Python CLI scaffold and tests | Preserve for the future `04-telemetry-detection` module. |
| `.github/workflows/` | build/sign, lint, Trivy scan, YAML validation | Preserve existing CI; add new checks only when useful. |

## Decision: Keep The Repo Name MERIDIAN

The public repository remains `MERIDIAN`, while the project identity becomes
MERIDIAN LABS. This avoids unnecessary repository churn while making the new
scope clear in documentation and lab folders.

## Decision: Broaden From Runtime Detection To Distributed Office Security

MERIDIAN v2 focused on Kubernetes runtime detection. That work is useful, but too
narrow for the new target roles. MERIDIAN LABS broadens the project into a
distributed office security lab covering segmentation, connectivity, hardening,
telemetry, detection, policy checks, and incident readiness.

## Decision: Preserve v2 Telemetry And Detection Work

The v2 material should not be deleted. Quickwit, Vector, Fluent Bit, Trivy, and
`meridian-detect` remain useful for telemetry and detection. They are retained as
future inputs to `labs/04-telemetry-detection/`.

## Decision: Documentation First, Implementation Second

The MVP should make the pivot understandable before adding code. This keeps the
project professional and avoids a large scaffold with no working behavior.

Implementation should follow the learning guardrail:

- Codex creates structure, docs, placeholders, and guided tasks.
- The repo owner implements the first real segmentation rules.
- The repo owner implements the first secure connectivity path.
- The repo owner implements the first hardening playbook.
- The repo owner implements the first parser/correlator.
- The repo owner implements the first policy check.

## Decision: Local-First Tooling

Docker, Ansible, Python, and GitHub Actions are appropriate only when they
support a specific lab objective. Heavy dependencies should be avoided until the
lab has a clear need and validation path.

## Decision: No Offensive Or External Targeting Scope

MERIDIAN LABS may include safe local traffic simulation and detection examples.
It must not include real credentials, external scanning, offensive tooling, or
instructions that target systems outside lab-owned local containers or virtual
machines.
