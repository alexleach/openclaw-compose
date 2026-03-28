# Setup

## Standalone

```bash
./scripts/bootstrap.sh
docker compose -f compose.openclaw.yaml up -d
```

## As an overlay in an existing project

If your project already has a `compose.yaml` or `compose.dev.yaml`, layer this file on top:

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml up -d openclaw
```

Then open a shell in the running container:

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml exec openclaw bash
```

## SSH profile

The compose file uses a shared OpenClaw service definition plus an SSH-enabled variant under the `ssh` profile.

If you want the container to have access to SSH keys too:

```bash
docker compose -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Suggested first-run steps inside the container

```bash
openclaw doctor
openclaw onboard
```

## What is preconfigured in the starter

The sample `openclaw/openclaw.json.example` includes:

- token auth on the gateway
- a conservative device/node deny-list
- a small multi-agent layout
- provider-based audio transcription as a portable default

The sample `.env.openclaw.example` also includes optional qmd and speech-related environment hints, but leaves them commented out so the overlay stays generic.

## Host project visibility

The host repo is mounted at `/workspace`, so OpenClaw can work directly against the checked-out project without copying source into the state volume.
