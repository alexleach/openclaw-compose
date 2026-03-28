# SSH profile recipe

Use this when OpenClaw needs read-only access to SSH keys inside the container.

## Start the SSH-enabled variant

```bash
docker compose -f compose.openclaw.yaml --profile ssh up -d openclaw-ssh
```

## Optional env override

In `.env.openclaw`:

```env
OPENCLAW_SSH_DIR=/home/your-user/.ssh
```

## Notes

- the SSH mount is read-only
- do not enable this unless you actually need it
- prefer the normal `openclaw` service when SSH access is unnecessary
