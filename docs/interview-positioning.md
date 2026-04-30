# Interview Positioning

MERIDIAN LABS is designed to be discussed as a practical security engineering
project, not as a finished product. The strongest signal is the decision trail:
what was modeled, what was intentionally simplified, what was validated, and
what tradeoffs were accepted.

## Network Security Operations

The project demonstrates network security operations by modeling:

- branch, HQ, guest, employee, service, admin, and cloud zones
- explicit allowed and denied flows
- secure branch-to-HQ connectivity
- validation steps for segmentation behavior
- telemetry that supports investigation instead of only deployment success
- problem-driven labs for trust boundaries, connectivity, telemetry, and
  automated validation

Good discussion points:

- why guest networks require separate trust assumptions
- how branch-to-branch access should be controlled
- what belongs at HQ versus the branch
- how to validate that a deny rule is actually enforced

## Infrastructure Security

The project demonstrates infrastructure security by showing:

- baseline host and service hardening plans
- separation of management interfaces from normal user paths
- retained security scanning with Trivy
- documentation of assumptions and limitations
- safe handling of secrets and local lab state
- baseline enforcement and drift-awareness thinking before broad automation

Good discussion points:

- how to stage hardening without over-automating too early
- how to reason about local-first labs versus production controls
- which controls are preventive, detective, or operational

## Security Automation

The project demonstrates security automation through:

- planned Ansible hardening after manual baseline work
- `meridian-detect` as a future telemetry and detection CLI
- lightweight scripts only where they clarify repeatable validation
- CI checks that support security review without becoming the primary artifact
- small validation rules tied to specific risks instead of a large policy
  platform introduced too early

Good discussion points:

- where automation is useful
- where manual implementation improves learning and design judgment
- how to keep automation reviewable and safe

## CI/CD Or GitOps Thinking

The project demonstrates CI/CD and GitOps thinking by:

- keeping infrastructure and security configuration in version control
- retaining GitHub Actions checks for linting, tests, YAML validation, and Trivy
- planning policy checks for unsafe configuration patterns
- documenting intended state before implementing broad automation

Good discussion points:

- how pull requests become a control point for security configuration
- why policy checks should start with narrow, explainable rules
- when a full GitOps platform would be premature

## Secure System Design

The project demonstrates secure design by documenting:

- trust boundaries
- assets and actors
- abuse cases and mitigations
- control-plane versus branch responsibilities
- technologies selected for the smallest useful implementation
- how each lab starts from an operational security problem rather than a tool
  selection exercise

Good discussion points:

- how a threat model changes after the first working lab
- what assumptions are acceptable for a portfolio lab
- which simplifications would not be acceptable in production

## Incident Response Readiness

The project demonstrates incident response readiness by planning for:

- central telemetry collection
- detection and enrichment workflows
- local, safe traffic simulation
- runbooks and investigation notes
- incident-response scenarios after baseline controls exist

Good discussion points:

- what evidence an analyst would need to investigate branch lateral movement
- how segmentation decisions affect response
- how detection gaps feed back into architecture changes
