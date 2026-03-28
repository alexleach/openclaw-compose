# Overlay into an existing Compose project

Use this when your app already has its own `compose.yaml` and you want OpenClaw alongside it.

## Start only OpenClaw from the combined stack

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml up -d openclaw
```

## Open a shell in the running container

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml exec openclaw bash
```

## SSH-enabled variant

```bash
docker compose -f compose.yaml -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Notes

- this keeps OpenClaw as an overlay rather than baking it into your main app image
- keep OpenClaw secrets in `.env.openclaw` rather than mixing them into the app's env if possible
