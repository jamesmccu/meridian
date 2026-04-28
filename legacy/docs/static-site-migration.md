# Static Site Migration

This document captures the plan for moving a static portfolio or documentation
site from managed static hosting into Meridian as a hosted service.

The site repository is expected to remain separate from this platform repository.
This document intentionally avoids local filesystem paths, private hostnames, and
deployment secrets because Meridian is public-facing.

Meridian should provide the runtime, ingress, TLS, deployment, and observability
foundation. The site repository should continue to own the site source code.

## Why This Is A Good First Hosted Service

A static site is a strong first workload for Meridian because it is:

- Real and externally useful.
- Low risk compared with a stateful or sensitive application.
- Easy to validate from the public internet.
- Good for proving ingress, DNS, TLS, deployment, logging, and rollback.
- A practical replacement for an existing managed hosting workflow.

## Migration Goals

- Host the site on the Meridian platform.
- Preserve the ability to build and test the site independently.
- Keep deployment declarative through GitOps.
- Add basic observability: uptime, access logs, deployment events, and resource
  usage.
- Keep rollback simple.
- Avoid coupling the site source repo tightly to the platform repo.

## Target Deployment Model

```text
static-site repository
        |
        v
Build workflow
  - install dependencies
  - build static site
  - build container image or static artifact
  - scan image/artifact
  - sign image when containerized
        |
        v
Container registry or artifact store
        |
        v
Meridian GitOps config
        |
        v
Homelab Kubernetes
  - Deployment or static web server
  - Service
  - Ingress
  - TLS certificate
  - logging and metrics
```

## Recommended Options

### Option 1: Containerized Static Site

Build the site into static files and serve it from a small Nginx or Caddy
container.

Benefits:

- Simple Kubernetes deployment.
- Easy rollback by image tag.
- Works well with Trivy and Cosign.
- Keeps runtime behavior close to other hosted services.

Tradeoffs:

- Requires an image build for each site release.
- Slightly more moving parts than object storage style hosting.

### Option 2: Static Artifact Served By Platform Web Server

Build the site as a static artifact and sync it to platform-managed storage or a
mounted volume served by Nginx/Caddy.

Benefits:

- Simple artifact model.
- No application container required.

Tradeoffs:

- Rollback and provenance are less clean unless artifact versioning is designed
  carefully.
- Less useful for learning container supply chain controls.

## Recommendation

Use Option 1 first: a containerized static site served by Nginx or Caddy.

Reason:

> It exercises the most platform capabilities with the least application risk:
> image build, vulnerability scan, signing, registry, GitOps deployment, ingress,
> TLS, logging, metrics, and rollback.

## Meridian Platform Requirements

Before migration, Meridian should have:

- Kubernetes runtime available in the homelab.
- Ingress controller.
- cert-manager or another TLS automation path.
- Public DNS plan.
- GitOps controller.
- Container registry access.
- Basic metrics and logs for the web workload.
- Rollback process documented.

## Cloudflare Decision

Cloudflare does not have to disappear immediately. A staged migration is safer:

1. Keep DNS managed where it is today.
2. Deploy the site privately inside Meridian.
3. Expose a test hostname.
4. Validate TLS, logs, health checks, rollback, and performance.
5. Move the production hostname after the platform path is proven.

Cloudflare can remain useful for DNS, proxying, or edge protections even if Pages
is no longer the hosting layer.

## Acceptance Criteria

- The site is deployed by GitOps, not by manual cluster edits.
- The public hostname serves the Meridian-hosted version.
- TLS is valid and renews automatically or has a documented renewal process.
- The deployment has a documented rollback path.
- Access logs are collected.
- Basic uptime or blackbox monitoring exists.
- The build artifact or image is scanned.
- The platform repo documents how the service is connected without embedding the
  full site source code.
