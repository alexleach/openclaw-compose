# Telegram recipe

Use this when you want direct personal access to OpenClaw from Telegram.

## 1. Create a bot

Use BotFather to create a bot and get a token.

## 2. Add the token

In `.env.openclaw`:

```env
TELEGRAM_BOT_TOKEN=...
```

## 3. Enable Telegram in OpenClaw config

In `openclaw/openclaw.json`:

```js
channels: {
  telegram: {
    enabled: true,
    dmPolicy: "pairing",
    groupPolicy: "allowlist",
    streaming: "partial",
  },
}
```

## 4. Start or restart OpenClaw

```bash
docker compose -f compose.openclaw.yaml up -d
```

## Suggested default policy

- keep DMs on `pairing`
- keep group access on `allowlist`
- start with direct personal use before adding groups

## Notes

Telegram is a good low-friction mobile-first channel for:

- quick questions
- reminders
- short coding requests
- voice notes if you enable transcription
