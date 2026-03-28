# Secrets and separation of concerns

Use a dedicated `.env.openclaw` file for the OpenClaw overlay.

That keeps:

- app/runtime secrets separate from
- OpenClaw gateway, model, and channel secrets

## Why this helps

- avoids accidental secret reuse across containers
- makes rotation easier
- reduces accidental leakage when open-sourcing
- keeps the assistant/tooling boundary obvious

## Suggested naming

- `.env.openclaw`
- `.env.openclaw.local`

If you embed this overlay inside another repository, keep the naming explicit so the boundary stays clear.
