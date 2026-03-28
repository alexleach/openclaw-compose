# Minimal recommendations

## Good defaults

- keep the compose file simple and close to upstream
- use a dedicated `.env.openclaw`
- use token auth on the gateway
- keep DMs on `pairing`
- keep group access on `allowlist`
- mount only the project workspace and persistent OpenClaw state

## Useful out-of-the-box additions

- enable audio transcription with a provider-backed default
- provide a small agent split (`main`, `frontend`, `backend`, `reviewer`)
- leave channel providers disabled until the user adds credentials
- document optional qmd/speech env hints without forcing them on everyone

## Things not worth enabling by default

- Docker socket access
- browser-heavy images
- broad public exposure
- lots of channel integrations at once

## Rollout advice

Start with:

1. one model provider
2. one messaging channel
3. the default agent split
4. audio transcription only if you actually use voice notes

Then add complexity only when the routing or workflow problem is real.
