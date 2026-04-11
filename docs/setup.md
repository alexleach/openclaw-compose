# Setup

This repo is designed to be dropped into an existing Compose project, not bootstrapped in place.

Use the README quick start for the recommended flow.

## If you are wiring OpenClaw into an app stack

1. Copy `.env.openclaw.example` to `.env.openclaw`
2. Copy `openclaw/openclaw.json.example` to `openclaw/openclaw.json`
3. Install the Python package with `pip install .` or `pip install -e .`
4. Generate a service with `openclaw-compose -f compose.yaml -o compose.openclaw.generated.yaml`
5. Start the combined stack with Docker Compose

## First run inside the container

```bash
openclaw doctor
openclaw onboard
```

## Host project visibility

The host repo is mounted at `/app`, so OpenClaw can work directly against the checked-out project without copying source into the state volume.
