# Segmentation Violation Runbook

Status: initial scaffold.

This runbook describes the intended response workflow for a segmentation
violation in MERIDIAN LABS. It is not backed by a complete running topology or
automated detection yet.

## Trigger

A network event or validation check indicates that traffic crossed a denied
boundary, such as guest access to a branch service or branch client access to a
telemetry management surface.

## Initial Triage

1. Identify the source zone, destination zone, action, protocol, and port.
2. Map the event to `network-security/segmentation/flows.yaml`.
3. Confirm whether the flow is expected to be denied.
4. Check whether the event is sample data, validation evidence, or observed
   runtime telemetry.

## Investigation Notes

- Confirm the affected platform domain.
- Review any available topology or Compose configuration.
- Check for recent policy, network, or service-catalog changes.
- Preserve command output or event samples as evidence.

## Containment Intent

- Keep guest and employee boundaries separated.
- Keep management interfaces reachable only from approved admin paths.
- Avoid broad route or firewall exceptions while investigating.

## Follow-Up

- Update validation evidence.
- Add or adjust detection fixtures if telemetry was missing.
- Feed confirmed lessons back into the threat model.
