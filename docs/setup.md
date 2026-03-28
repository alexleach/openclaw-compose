# Setup

## Standalone

```bash
cp .env.openclaw.example .env.openclaw
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

The compose file uses a YAML anchor for the shared OpenClaw service definition, then adds an SSH-enabled variant under the `ssh` profile.

If you want the container to have access to SSH keys too:

```bash
docker compose -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Suggested first-run steps inside the container

```bash
openclaw doctor
openclaw onboard
```

## Host project visibility

The host repo is mounted at `/workspace`.

That means OpenClaw can work directly against the checked-out project without copying source into the state volume.
