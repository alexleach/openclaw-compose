# openclaw-compose

Portable Docker Compose overlay for adding OpenClaw to an existing project.

It gives you a clean OpenClaw sidecar that mounts your host repo at `/app`, keeps OpenClaw state in a named volume, and keeps assistant-specific config separate from your app stack.

## What you get

- one main `openclaw` service
- optional `openclaw-ssh` variant under the `ssh` profile
- persistent OpenClaw state in a named Docker volume
- host project mounted into `/app`
- separate OpenClaw env/config examples
- a small bootstrap script for first run

## Mental model

```text
Host project repo
  └─ mounted at /app inside OpenClaw

Compose services
  ├─ openclaw
  ├─ openclaw-ssh (optional)
  └─ openclaw_state volume

Chats / clients
  └─ talk to OpenClaw
```

## Repository layout

- `compose.openclaw.yaml` — Compose overlay
- `.env.openclaw.example` — env template
- `openclaw/openclaw.json.example` — starter OpenClaw config
- `scripts/bootstrap.sh` — first-run helper
- `docs/` — setup, security, secrets, and recommendations

## Quick start

```bash
./scripts/bootstrap.sh
```

Then:

1. edit `.env.openclaw`
2. review `openclaw/openclaw.json`
3. start OpenClaw:

```bash
docker compose -f compose.openclaw.yaml up -d
```

4. open a shell in the running container:

```bash
docker compose -f compose.openclaw.yaml exec openclaw bash
```

5. finish onboarding inside the container:

```bash
openclaw doctor
openclaw onboard
```

## Use as an overlay in another project

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml up -d openclaw
```

For the SSH-enabled variant:

```bash
docker compose -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

Or layered onto another project:

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Design notes

This starter stays intentionally close to the upstream OpenClaw image:

- no custom `command`
- no custom `healthcheck`
- no extra helper container by default
- one shared service definition with an SSH-profile variant

That keeps the overlay small and avoids fighting upstream container behaviour.

## State model

This setup separates:

- **OpenClaw state** in a named Docker volume
- **project source** mounted from the host into `/app`

That gives you durable sessions/config without copying your source tree into the OpenClaw state volume.

## Security defaults

This repository deliberately does **not** enable by default:

- Docker socket access
- browser-heavy extras
- hard-coded secrets
- public unauthenticated gateway access

## Included starter config

The sample `openclaw/openclaw.json.example` includes:

- token-authenticated gateway config
- conservative node/device command denial
- a small multi-agent split
- audio transcription enabled with a provider-backed default
- channel configs left disabled until you add real credentials

## Docs

- Setup: `docs/setup.md`
- Security: `docs/security.md`
- Secrets: `docs/secrets.md`
- Recommendations: `docs/recommendations.md`
- Agents and channels: `docs/agents-and-channels.md`
- Recipes:
  - `docs/recipes/discord.md`
  - `docs/recipes/telegram.md`
  - `docs/recipes/tailscale.md`
  - `docs/recipes/ollama.md`
  - `docs/recipes/ssh-profile.md`
  - `docs/recipes/overlay-existing-project.md`
- OpenClaw Docker docs: <https://docs.openclaw.ai/install/docker>
- OpenClaw config docs: <https://docs.openclaw.ai/gateway/configuration>
