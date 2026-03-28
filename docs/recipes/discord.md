# Discord recipe

Use this when you want OpenClaw reachable through a Discord bot.

## 1. Create a bot application

In the Discord developer portal:

- create an application
- add a bot user
- copy the bot token
- enable the intents you actually need

## 2. Add the token

In `.env.openclaw`:

```env
DISCORD_BOT_TOKEN=...
```

## 3. Enable Discord in OpenClaw config

In `openclaw/openclaw.json`:

```js
channels: {
  discord: {
    enabled: true,
    dmPolicy: "pairing",
    groupPolicy: "allowlist",
    streaming: "off",
  },
}
```

## 4. Start or restart OpenClaw

```bash
docker compose -f compose.openclaw.yaml up -d
```

## 5. Invite the bot

Invite the bot to your server with only the permissions it actually needs.

## Suggested default policy

- keep DMs on `pairing`
- keep group access on `allowlist`
- require mention in group channels if that fits your setup
- start with one server, not all of them

## Notes

- native provider slash-command registration is separate from simply receiving messages
- keep the bot token out of committed files
