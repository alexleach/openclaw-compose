# Secrets and separation of concerns

You raised a fair point: OpenClaw secrets are not always the same concern as the host application's own runtime secrets.

## Recommendation

Use a dedicated `.env.openclaw` file for the OpenClaw overlay repository.

That keeps:

- project application env separate from
- OpenClaw gateway / model / channel env

If you embed this overlay directly inside another repository, keep the naming explicit so the boundary stays obvious.
Examples:

- `.env.openclaw`
- `.env.openclaw.local`
- `docker compose --env-file .env.openclaw ...`

## Why this is better

- avoids mixing application secrets with assistant/tooling secrets
- makes rotation easier
- reduces accidental reuse in app containers
- makes open-sourcing safer

## Practical note

This starter uses `.env.openclaw` as the recommended default so the OpenClaw boundary stays explicit.
