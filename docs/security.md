# Security notes

## Defaults in this starter

This template does **not** enable by default:

- Docker socket access
- browser-heavy extras
- hard-coded API keys or bot tokens
- public unauthenticated gateway access

It also starts with a few conservative OpenClaw config choices:

- `gateway.auth.mode: "token"`
- `gateway.tailscale.mode: "off"`
- `channels.*.dmPolicy: "pairing"`
- `channels.*.groupPolicy: "allowlist"`
- conservative `gateway.nodes.denyCommands`

## Secrets handling

Keep secrets in `.env.openclaw` or your shell environment.
Do not commit them into:

- `compose.openclaw.yaml`
- `openclaw/openclaw.json`
- README examples
- other checked-in docs or helper files

## Minimum secure defaults

1. keep gateway auth enabled
2. prefer pairing for DMs
3. prefer allowlists for groups/channels
4. gate risky device/node actions unless you need them
5. do not commit channel tokens or model-provider keys
6. avoid Docker socket access by default
7. only expose the gateway deliberately

## Gateway token

Generate a token with:

```bash
openssl rand -hex 32
```

## If exposing the gateway remotely

- keep token or password auth enabled
- prefer an authenticated tunnel such as Tailscale
- do not rely on obscurity or a high port alone
