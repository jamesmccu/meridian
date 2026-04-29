# Learning Map

MERIDIAN LABS is optimized for practical security architecture and engineering
practice across distributed branch offices, HQ services, and cloud dependencies.

## Primary Skill Targets

| Area | MERIDIAN LABS Practice |
|---|---|
| Network security | Model zones, routes, allowed flows, denied flows, and branch-to-HQ access. |
| Infrastructure security | Apply host and service hardening after defining the baseline topology. |
| Security automation | Use scripts, Ansible, and CI checks where they make controls repeatable. |
| Telemetry and detection | Preserve and extend v2 event pipeline and `meridian-detect` work. |
| Secure system design | Document trust boundaries, abuse cases, assumptions, and limitations. |
| Incident readiness | Build detection evidence and runbooks from local, safe scenarios. |

## What To Build Personally

The highest-learning work should be done by the repo owner:

- first firewall or segmentation rules
- first VPN or secure connectivity implementation
- first Ansible hardening playbook
- first Python log parser or correlator
- first GitHub Actions policy check
- first threat-model refinement after observing the working lab
- first architecture diagram after the topology is understood

## What Can Be Mechanical Cleanup

Lower-learning-value work:

- moving old positioning into the new documentation structure
- creating lab folders and placeholder READMEs
- writing guided task prompts
- keeping CI and public hygiene clean

## Proof Of Competence

A strong MERIDIAN LABS module should show the full loop:

```text
design intent -> implementation -> validation -> telemetry -> documented tradeoff
```

One complete validated control path is more valuable than many untested tools.
