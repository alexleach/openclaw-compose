# Setup

## Standalone

```bash
cp .env.openclaw.example .env.openclaw
docker compose --env-file .env.openclaw -f compose.openclaw.yaml --profile openclaw up -d
```

## As an overlay in an existing project

If your project already has a `compose.yaml` or `compose.dev.yaml`, layer this file on top:

```bash
docker compose --env-file .env.openclaw -f compose.yaml -f compose.openclaw.yaml --profile openclaw up -d openclaw-gateway
```

Then open the CLI container:

```bash
docker compose --env-file .env.openclaw -f compose.yaml -f compose.openclaw.yaml run --rm openclaw-cli bash
```

## Suggested first-run steps inside the CLI container

```bash
openclaw doctor
openclaw onboard
```

## Host project visibility

The host repo is mounted at `/workspace`.

That means OpenClaw can work directly against the checked-out project without copying source into the state volume.
