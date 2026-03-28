# openclaw-compose

Drop OpenClaw into any Docker Compose project.

`openclaw-compose` is a minimal Compose overlay for running OpenClaw alongside an existing app without baking assistant-specific concerns into the main stack.

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

## Quick start

```bash
./scripts/bootstrap.sh
docker compose -f compose.openclaw.yaml up -d
docker compose -f compose.openclaw.yaml exec openclaw bash
```

Then inside the container:

```bash
openclaw doctor
openclaw onboard
```

## Why this exists

- keep OpenClaw separate from your app container
- keep OpenClaw state in a named volume
- mount your checked-out project into the container at `/app`
- keep OpenClaw env/config separate from app secrets
- stay close to the upstream OpenClaw image

## Common usage

### Standalone

```bash
docker compose -f compose.openclaw.yaml up -d
```

### Overlay on an existing Compose project

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml up -d openclaw
```

### SSH-enabled variant

```bash
docker compose -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Docs

- [Setup](docs/setup.md)
- [Security](docs/security.md)
- [Secrets](docs/secrets.md)
- [Recommendations](docs/recommendations.md)
- [Agents and channels](docs/agents-and-channels.md)
- Recipes:
  - [Discord](docs/recipes/discord.md)
  - [Telegram](docs/recipes/telegram.md)
  - [Tailscale / private remote access](docs/recipes/tailscale.md)
  - [Ollama / OpenAI-compatible models](docs/recipes/ollama.md)
  - [SSH profile](docs/recipes/ssh-profile.md)
  - [Overlay into an existing Compose project](docs/recipes/overlay-existing-project.md)

## Upstream docs

- [OpenClaw Docker docs](https://docs.openclaw.ai/install/docker)
- [OpenClaw config docs](https://docs.openclaw.ai/gateway/configuration)
