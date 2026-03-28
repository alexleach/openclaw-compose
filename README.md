# openclaw-compose

Portable Docker Compose overlay for adding an OpenClaw workspace and gateway sidecar to an existing project.

## What this is

This repository gives you a reusable OpenClaw sidecar setup you can drop into another Docker Compose project without baking assistant-specific concerns into the app stack itself.

It is designed to:

- keep OpenClaw state persistent
- mount the host project at `/workspace`
- keep OpenClaw secrets separate from app secrets
- provide a clean first-run bootstrap path
- stay safe by default

## Repository layout

- `compose.openclaw.yaml` — main Compose overlay
- `compose.openclaw.ssh.yaml` — optional SSH mount overlay
- `.env.openclaw.example` — environment template
- `scripts/bootstrap.sh` — first-run bootstrap helper
- `openclaw/openclaw.json.example` — starter OpenClaw config
- `docs/` — setup, security, agents/channels, and secrets guidance

## Quick start

### 1. Bootstrap

```bash
./scripts/bootstrap.sh
```

That will:

- create `.env.openclaw` from `.env.openclaw.example` if missing
- generate an `OPENCLAW_GATEWAY_TOKEN`
- create `openclaw/openclaw.json` from the example if missing

### 2. Add secrets

Edit `.env.openclaw` and add whichever provider or channel credentials you actually use.

### 3. Start OpenClaw

```bash
docker compose --env-file .env.openclaw -f compose.openclaw.yaml --profile openclaw up -d
```

### 4. Open the CLI container

```bash
docker compose --env-file .env.openclaw -f compose.openclaw.yaml run --rm openclaw-cli bash
```

### 5. Finish onboarding

Inside the container:

```bash
openclaw doctor
openclaw onboard
```

## Using this as an overlay in another project

If the target project already has its own Compose file:

```bash
docker compose --env-file .env.openclaw -f compose.yaml -f compose.openclaw.yaml --profile openclaw up -d openclaw-gateway
```

If you want SSH available inside the OpenClaw containers too:

```bash
docker compose --env-file .env.openclaw -f compose.yaml -f compose.openclaw.yaml -f compose.openclaw.ssh.yaml --profile openclaw --profile openclaw-ssh up -d
```

## State model

This setup intentionally separates:

- **OpenClaw state** in a named Docker volume
- **project source** mounted from the host into `/workspace`

That gives you durable sessions/config without copying your actual source tree into the OpenClaw state volume.

## Recommended secret boundary

You were right to question whether OpenClaw secrets belong in the same env file as the host application.

For a real project, I recommend using a dedicated env file such as:

- `.env.openclaw`
- `.env.openclaw.local`

Then run Compose with:

```bash
docker compose --env-file .env.openclaw -f compose.openclaw.yaml --profile openclaw up -d
```

This starter uses `.env.openclaw` as the default boundary so OpenClaw secrets stay clearly separate from the host application's own env.

## Suggested agent layout for full-stack projects

A sensible default is:

- `main`
- `frontend`
- `backend`
- `reviewer`

That split is already reflected in `openclaw/openclaw.json.example`.

## Security defaults

This repository deliberately does **not** enable by default:

- Docker socket access
- browser dependencies
- hard-coded secrets
- public unauthenticated gateway access

## Publish checklist

Before publishing, verify that you have not committed:

- real API keys
- channel tokens
- personal phone numbers
- private hostnames
- copied state from `~/.openclaw`

## Docs

- Setup: `docs/setup.md`
- Security: `docs/security.md`
- Secrets: `docs/secrets.md`
- Agents and channels: `docs/agents-and-channels.md`
- OpenClaw Docker docs: <https://docs.openclaw.ai/install/docker>
- OpenClaw config docs: <https://docs.openclaw.ai/gateway/configuration>
- OpenClaw models docs: <https://docs.openclaw.ai/concepts/models>
