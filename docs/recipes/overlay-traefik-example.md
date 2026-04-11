# Traefik example

This example shows a small Compose app with Traefik and a simple nginx web service.

## Input compose file

`examples/traefik-web/compose.yaml`

```yaml
name: traefik-web

services:
  traefik:
    image: traefik:v3.1
    command:
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --entrypoints.web.address=:80
      - --api.dashboard=true
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    labels:
      - traefik.enable=true
      - traefik.http.routers.dashboard.rule=Host(`traefik.localhost`)
      - traefik.http.routers.dashboard.service=api@internal

  web:
    image: nginx:1.27-alpine
    volumes:
      - ./site:/usr/share/nginx/html:ro
    labels:
      - traefik.enable=true
      - traefik.http.routers.web.rule=Host(`web.localhost`)
      - traefik.http.routers.web.entrypoints=web
      - traefik.http.services.web.loadbalancer.server.port=80
```

## Generated overlay

Actual output from:

```bash
openclaw-compose -f examples/traefik-web/compose.yaml --service web -o compose.openclaw.generated.yaml
```

```yaml
name: openclaw-compose
services:
  openclaw:
    extends:
      file: compose.yaml
      service: web
    volumes:
      - ./site:/usr/share/nginx/html:ro
      - type: bind
        source: /home/appuser/.openclaw
        target: /home/node/.openclaw
    labels:
      - traefik.enable=true
      - traefik.http.routers.web.rule=Host(`web.localhost`)
      - traefik.http.routers.web.entrypoints=web
      - traefik.http.services.web.loadbalancer.server.port=80
```

## Notes

- The parent service's volume wiring is preserved.
- OpenClaw adds only the mounts you explicitly enable.
- This example keeps Traefik in the parent stack and layers OpenClaw onto the `web` service.
