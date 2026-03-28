# Security notes

## Defaults in this starter

This template intentionally does **not** include:

- Docker socket access
- browser-heavy dependencies
- hard-coded API keys
- hard-coded bot tokens
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
- devcontainer examples

## Minimal secure-by-default recommendations

These are the sensible low-friction defaults from the current OpenClaw docs:

1. **Keep gateway auth enabled**
   - if the gateway binds beyond loopback, use a strong token
2. **Prefer pairing for DMs**
   - unknown senders should not get direct access by default
3. **Prefer allowlists for groups/channels**
   - especially on Discord, Telegram, Matrix, and Slack
4. **Disable risky device/node actions unless you need them**
   - camera, screen recording, and write-actions are worth gating
5. **Do not commit channel tokens or provider keys**
   - obvious, but still the most common failure mode
6. **Avoid enabling Docker socket access by default**
   - it is a major trust-boundary expansion
7. **Only enable public exposure deliberately**
   - if later using Tailscale Serve/Funnel or other ingress, review auth again

## Token requirement

Generate a gateway token with:

```bash
openssl rand -hex 32
```

## Notes on remote exposure

If you later expose the gateway remotely:

- keep token/password auth on
- prefer Tailscale or another authenticated tunnel
- do not rely on obscurity or a high port alone
