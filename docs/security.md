# Security notes

## Defaults

This template intentionally does **not** include:

- Docker socket mount
- SSH key mount
- hard-coded API keys
- hard-coded bot tokens
- public unauthenticated gateway access

## Secrets handling

Keep secrets in `.env` or in your shell environment.
Do not commit them into:

- `compose.openclaw.yaml`
- `devcontainer.json`
- `openclaw.json`
- README examples

## Token requirement

If `OPENCLAW_GATEWAY_BIND=lan`, set a strong `OPENCLAW_GATEWAY_TOKEN`.

Generate one with:

```bash
openssl rand -hex 32
```

## Optional privileged features

If you later enable Docker socket access for sandboxing, do it explicitly and document it for the target project.
That is a meaningful trust boundary expansion.
