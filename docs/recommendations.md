# Minimal recommendations

These are the short practical recommendations I’d make based on the current OpenClaw docs and your usage pattern.

## Good defaults

- keep the compose file simple and close to upstream
- use a dedicated `.env.openclaw`
- use token auth on the gateway
- keep DM access on `pairing`
- keep group access on `allowlist`
- mount only the project workspace and persistent OpenClaw state

## Useful out-of-the-box additions

- enable audio transcription with a provider-backed default
- provide a starter multi-agent split (`main`, `frontend`, `backend`, `reviewer`)
- leave channel providers disabled until the user fills in tokens
- document qmd-related env hints, but don’t force them on everyone

## Things not worth enabling by default

- Docker socket access
- browser-heavy images
- broad public exposure
- lots of channel integrations at once

## Practical rollout advice

Start with:

1. one model provider
2. one messaging channel
3. the default agent split
4. audio transcription only if you actually use voice notes

Then add complexity only when the routing or workflow problem is real.
