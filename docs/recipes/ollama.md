# Ollama / OpenAI-compatible local model recipe

Use this when you want OpenClaw to talk to a local or self-hosted OpenAI-compatible model endpoint.

## 1. Add endpoint env

In `.env.openclaw`:

```env
OPENAI_BASE_URL=http://host.docker.internal:11434/v1
OLLAMA_URL=http://host.docker.internal:11434
```

Adjust the host and port to match your setup.

## 2. Add provider config if needed

If your OpenClaw config needs an explicit provider entry, add one in `openclaw/openclaw.json`.

## 3. Start or restart OpenClaw

```bash
docker compose -f compose.openclaw.yaml up -d
```

## Notes

- `host.docker.internal` is convenient on Docker Desktop and some Linux setups, but not universal
- if that hostname does not resolve in your environment, use the correct host bridge or reachable IP instead
- keep the first test simple before adding multiple providers or fallback chains
