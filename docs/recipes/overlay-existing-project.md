# Add OpenClaw to an existing Compose project

Use this when your app already has its own `compose.yaml` and you want OpenClaw alongside it.

## Generate a service

```bash
openclaw-compose -f compose.yaml -o compose.openclaw.generated.yaml
```

If your project has multiple services, the CLI will prompt you to pick one unless you pass `--service`.

## What the generator does

- reads the parent compose file
- creates a new service that `extends` the selected app service
- adds only the OpenClaw mounts you explicitly request
- writes a separate file instead of editing your app stack in place

## Start OpenClaw from the combined stack

```bash
docker compose -f compose.yaml -f compose.openclaw.generated.yaml up -d openclaw
```

## Open a shell in the running container

```bash
docker compose -f compose.yaml -f compose.openclaw.generated.yaml exec openclaw bash
```

## Notes

- this keeps OpenClaw separate from your app image for now
- keep OpenClaw secrets in `.env.openclaw` rather than mixing them into the app's env if possible
