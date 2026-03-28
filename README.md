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

## Design choices

This starter now stays intentionally close to the upstream OpenClaw image, while using a small YAML anchor to keep the SSH variant tidy:

- no custom `command`
- no custom `healthcheck`
- no extra `HOME` / `TERM` / `TZ` defaults
- no separate CLI sidecar by default
- one main service, plus an SSH-profile variant when you explicitly want key access
- YAML anchors for the shared service definition

That keeps the compose file smaller and avoids fighting upstream container behavior.

## Repository layout

- `compose.openclaw.yaml` — main Compose overlay
- `.env.openclaw.example` — environment template
- `scripts/bootstrap.sh` — first-run bootstrap helper
- `openclaw/openclaw.json.example` — starter OpenClaw config
- `docs/` — setup, security, recommendations, agents/channels, and secrets guidance

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

The starter env file now also includes:

- qmd-related env hints for retrieval-backed workflows
- STT/TTS-related env hints
- Azure / OpenAI-compatible provider examples

### 3. Start OpenClaw

```bash
docker compose -f compose.openclaw.yaml up -d
```

### 4. Open a shell in the running container

```bash
docker compose -f compose.openclaw.yaml exec openclaw bash
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
docker compose -f compose.yaml -f compose.openclaw.yaml up -d openclaw
```

If you want SSH available inside the OpenClaw container too:

```bash
docker compose -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

Or when layering onto another project:

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Why the earlier version had extra pieces

Your comments were fair. The first draft was more defensive than necessary.

- `init: true` adds a tiny init process for signal handling and zombie reaping. Useful sometimes, but not essential here.
- a separate CLI container only really helps if you want shared-network localhost access while keeping the main service immutable.
- a third browser-oriented service was overkill for this project.

For this starter, simpler is better. YAML anchors give us a bit of DRY without introducing another compose file or `extends` quirks.

## env_file vs --env-file

I agree with you that service-level `env_file` is cleaner here.

This repo now uses:

```yaml
env_file:
  - ./.env.openclaw
```

That means you usually do **not** need to pass `--env-file` on the command line.

## State model

This setup intentionally separates:

- **OpenClaw state** in a named Docker volume
- **project source** mounted from the host into `/workspace`

That gives you durable sessions/config without copying your actual source tree into the OpenClaw state volume.

## Included starter config

The sample `openclaw/openclaw.json.example` now includes a few practical defaults:

- token-authenticated gateway config
- conservative node/device command denial
- a small multi-agent split
- audio transcription enabled with a portable provider-backed default
- channel configs left disabled until you add real credentials

It is meant to be useful immediately without hard-coding your personal infrastructure.

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
- Recommendations: `docs/recommendations.md`
- Secrets: `docs/secrets.md`
- Agents and channels: `docs/agents-and-channels.md`
- OpenClaw Docker docs: <https://docs.openclaw.ai/install/docker>
- OpenClaw config docs: <https://docs.openclaw.ai/gateway/configuration>
- OpenClaw models docs: <https://docs.openclaw.ai/concepts/models>
