# Tailscale / private remote access recipe

Use this when you want remote access without exposing OpenClaw directly to the public internet.

## Suggested approach

Prefer an authenticated private network or tunnel such as Tailscale.

## Minimum advice

- keep gateway auth enabled
- use a strong token
- do not rely on a high port alone
- avoid making the gateway publicly reachable unless you have reviewed the security model

## High-level flow

1. get OpenClaw working locally first
2. put the host on your private network / tailnet
3. expose access deliberately
4. test from a second device
5. review auth and access policies again

## Notes

This repo does not try to fully automate remote exposure. That is intentional.
