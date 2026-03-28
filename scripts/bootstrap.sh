#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f .env.openclaw ]]; then
  cp .env.openclaw.example .env.openclaw
  echo "Created .env.openclaw from .env.openclaw.example"
else
  echo ".env.openclaw already exists"
fi

mkdir -p openclaw

if [[ ! -f openclaw/openclaw.json ]]; then
  cp openclaw/openclaw.json.example openclaw/openclaw.json
  echo "Created openclaw/openclaw.json from example"
else
  echo "openclaw/openclaw.json already exists"
fi

if grep -q 'OPENCLAW_GATEWAY_TOKEN=replace-me' .env.openclaw; then
  export TOKEN="$(openssl rand -hex 32)"
  if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY'
from pathlib import Path
p = Path('.env.openclaw')
text = p.read_text()
import os
text = text.replace('OPENCLAW_GATEWAY_TOKEN=replace-me', f"OPENCLAW_GATEWAY_TOKEN={os.environ['TOKEN']}")
p.write_text(text)
PY
  else
    sed -i.bak "s/OPENCLAW_GATEWAY_TOKEN=replace-me/OPENCLAW_GATEWAY_TOKEN=${TOKEN}/" .env.openclaw && rm -f .env.openclaw.bak
  fi
  echo "Generated OPENCLAW_GATEWAY_TOKEN in .env.openclaw"
fi

cat <<'EOF'

Bootstrap complete.

Next steps:
  1. Edit .env.openclaw and add any provider/channel secrets you need
  2. Review openclaw/openclaw.json
  3. Start OpenClaw:
     docker compose --env-file .env.openclaw -f compose.openclaw.yaml --profile openclaw up -d
  4. Open a shell:
     docker compose --env-file .env.openclaw -f compose.openclaw.yaml run --rm openclaw-cli bash
  5. Inside the container, run:
     openclaw doctor
     openclaw onboard

Optional SSH mount:
  docker compose --env-file .env.openclaw -f compose.openclaw.yaml -f compose.openclaw.ssh.yaml --profile openclaw --profile openclaw-ssh up -d
EOF
