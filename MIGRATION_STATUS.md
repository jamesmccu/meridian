# Meridian Migration Status

This file tracks the monorepo-to-multi-repo split for Meridian.

## Target Repositories

- `meridian-platform`
- `meridian-api`
- `meridian-web`
- `meridian-security`
- `meridian-docs`

## Migration Rules

- `MERIDIAN` remains the umbrella repo and architecture entry point.
- Domain code/config should have one canonical home in a split repo.
- During transition, references in `MERIDIAN` should point to canonical files.

## Folder Migration Map

| Source Path in `MERIDIAN` | Target Repo | Status | Notes |
|---|---|---|---|
| `aws/` | `meridian-platform` | not_started | Cloud infra/config ownership moves to platform repo. |
| `onprem/` | `meridian-platform` | not_started | On-prem stack and related configs. |
| `gitops/` | `meridian-platform` | not_started | GitOps and deployment scaffolding. |
| `observability/` | `meridian-platform` | not_started | Shared telemetry pipeline and configs. |
| `tools/` | `meridian-platform` | not_started | Platform automation and shared libraries. |
| `security/` | `meridian-security` | not_started | Security controls and enforcement assets. |
| `README.md` (architecture sections) | `meridian-docs` | in_progress | Keep top-level summary in umbrella repo. |
| `STRUCTURE.md` | `meridian-docs` | not_started | Canonical structure docs move to docs repo. |
| `CHANGELOG.md` | `meridian-docs` | not_started | Change history for split components. |
| `RELEASE_NOTES.md` | `meridian-docs` | not_started | Release narratives and milestones. |
| App/backend components (future extraction) | `meridian-api` | not_started | Extract when service code exists in monorepo. |
| Frontend/dashboard components (future extraction) | `meridian-web` | not_started | Includes `dashboard` migration destination. |

## Umbrella Repo Keep List (`MERIDIAN`)

- High-level architecture narrative
- Cross-repo topology and navigation
- Migration status tracking
- Portfolio-level context and outcomes

## Completion Checklist

- [x] Create split repos and initialize scopes
- [x] Link split repos from `MERIDIAN` README
- [ ] Migrate platform folders (`aws`, `onprem`, `gitops`, `observability`, `tools`)
- [ ] Migrate security folder (`security`)
- [ ] Migrate docs artifacts (`STRUCTURE.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`)
- [ ] Add cross-repo CI/standards references
- [ ] Remove duplicated content from `MERIDIAN`
