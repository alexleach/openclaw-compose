#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any
import textwrap

import typer
import yaml

app = typer.Typer(add_completion=False, invoke_without_command=True, help="Generate an OpenClaw Compose service for an existing app.")

DEFAULT_OUTPUT = Path("compose.openclaw.generated.yaml")
DEFAULT_COMPOSE_FILES = [Path("compose.yaml")]
DEFAULT_HOST_OPENCLAW_HOME = Path.home() / ".openclaw"
DEFAULT_CONTAINER_OPENCLAW_HOME = "/home/node/.openclaw"
DEFAULT_CONTAINER_BASHRC = "/home/node/.bashrc"
DEFAULT_CONTAINER_CLAUDE = "/home/node/.claude"
DEFAULT_CONTAINER_CODEX = "/home/node/.codex"
DEFAULT_CONTAINER_SSH = "/home/node/.ssh"
OPENCLAW_SERVICE = "openclaw"
OPENCLAW_IMAGE = "ghcr.io/openclaw/openclaw:latest"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise typer.BadParameter(f"{path} is not a valid Compose document")
    return data


def _service_names(compose: dict[str, Any]) -> list[str]:
    services = compose.get("services", {})
    if isinstance(services, dict):
        return list(services.keys())
    return []


def _pick_service(services: list[str]) -> str:
    if len(services) == 1:
        return services[0]
    typer.echo("Available services:")
    for idx, name in enumerate(services, start=1):
        typer.echo(f"  {idx}. {name}")
    choice = typer.prompt("Select a service", type=int)
    if choice < 1 or choice > len(services):
        raise typer.BadParameter("invalid service selection")
    return services[choice - 1]


def _normalize_volume(item: Any) -> Any:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return dict(item)
    return item


def _bind(source: Path, target: str, read_only: bool = False) -> dict[str, Any]:
    item: dict[str, Any] = {"type": "bind", "source": str(source), "target": target}
    if read_only:
        item["read_only"] = True
    return item


def _merge_unique_volumes(base: list[Any], extras: list[Any]) -> list[Any]:
    seen: set[str] = set()
    merged: list[Any] = []
    for item in base + extras:
        key = yaml.safe_dump(item, sort_keys=True) if not isinstance(item, str) else item
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged


def _compose_dir(path: Path) -> Path:
    return path.resolve().parent


def _compose_project_name(compose: dict[str, Any], compose_path: Path) -> str:
    name = compose.get("name")
    if isinstance(name, str) and name.strip():
        return name.strip()
    return compose_path.parent.name


def _compose_base_image(service: dict[str, Any], project_name: str, service_name: str) -> str | None:
    image = service.get("image")
    if isinstance(image, str) and image:
        return image

    build = service.get("build")
    if isinstance(build, dict):
        image = build.get("image")
        if isinstance(image, str) and image:
            return image
        return f"{project_name}-{service_name}"

    if isinstance(build, str) and build:
        return f"{project_name}-{service_name}"

    return None


def _build_context(service: dict[str, Any], compose_path: Path) -> str:
    build = service.get("build")
    if isinstance(build, str) and build:
        return str((_compose_dir(compose_path) / build).resolve())
    if isinstance(build, dict):
        context = build.get("context")
        if isinstance(context, str) and context:
            return str((_compose_dir(compose_path) / context).resolve())
    return str(_compose_dir(compose_path))


def _dockerfile_inline(base_image: str, mount_ssh: bool) -> str:
    ssh_lines = "\nRUN mkdir -p /home/node/.ssh && chmod 700 /home/node/.ssh" if mount_ssh else ""
    return textwrap.dedent(
        f"""
        FROM {base_image}

        USER root
        RUN python3 -m pip install --no-cache-dir {OPENCLAW_IMAGE}{ssh_lines}
        USER node
        """
    ).strip() + "\n"


def build_overlay(
    compose_path: Path,
    target_service: str,
    host_openclaw_home: Path,
    mount_bashrc: bool,
    mount_codex: bool,
    mount_claude: bool,
    mount_ssh: bool,
) -> dict[str, Any]:
    compose = _load_yaml(compose_path)
    services = compose.get("services", {})
    if not isinstance(services, dict) or target_service not in services:
        raise typer.BadParameter(f"service {target_service!r} not found in {compose_path}")

    project_name = _compose_project_name(compose, compose_path)
    base = services[target_service]
    if not isinstance(base, dict):
        raise typer.BadParameter(f"service {target_service!r} is malformed")

    base_volumes = [_normalize_volume(v) for v in base.get("volumes", []) if v is not None]
    extra_volumes: list[Any] = [_bind(host_openclaw_home, DEFAULT_CONTAINER_OPENCLAW_HOME)]

    if mount_bashrc:
        extra_volumes.append(_bind(Path.home() / ".bashrc", DEFAULT_CONTAINER_BASHRC, read_only=True))
    if mount_codex:
        extra_volumes.append(_bind(Path.home() / ".codex", DEFAULT_CONTAINER_CODEX))
    if mount_claude:
        extra_volumes.append(_bind(Path.home() / ".claude", DEFAULT_CONTAINER_CLAUDE))
    if mount_ssh:
        extra_volumes.append(_bind(Path.home() / ".ssh", DEFAULT_CONTAINER_SSH, read_only=True))

    base_image = _compose_base_image(base, project_name, target_service)
    if base_image is None:
        raise typer.BadParameter(f"service {target_service!r} must define image or build metadata")

    overlay_service: dict[str, Any] = {
        "extends": {"file": compose_path.name, "service": target_service},
        "build": {
            "context": _build_context(base, compose_path),
            "dockerfile_inline": _dockerfile_inline(base_image, mount_ssh),
        },
        "volumes": _merge_unique_volumes(base_volumes, extra_volumes),
    }

    if "command" in base:
        overlay_service["command"] = base["command"]
    if "entrypoint" in base:
        overlay_service["entrypoint"] = base["entrypoint"]
    if "working_dir" in base:
        overlay_service["working_dir"] = base["working_dir"]
    if "user" in base:
        overlay_service["user"] = base["user"]

    return {"name": "openclaw-compose", "services": {OPENCLAW_SERVICE: overlay_service}}


@app.callback(invoke_without_command=True)
def main(
    file: Annotated[list[Path], typer.Option("-f", "--file", exists=True, readable=True, help="Compose file(s) to inspect.")] = DEFAULT_COMPOSE_FILES,
    output: Annotated[Path, typer.Option("-o", "--output", help="Output overlay file.")] = DEFAULT_OUTPUT,
    service: Annotated[str | None, typer.Option("--service", help="Target service name.")] = None,
    openclaw_home: Annotated[Path, typer.Option("--openclaw-home", help="Host OpenClaw home to mount.")] = DEFAULT_HOST_OPENCLAW_HOME,
    mount_bashrc: Annotated[bool, typer.Option("--mount-bashrc", help="Mount ~/.bashrc into the container.")] = False,
    mount_codex: Annotated[bool, typer.Option("--mount-codex", help="Mount ~/.codex into the container.")] = False,
    mount_claude: Annotated[bool, typer.Option("--mount-claude", help="Mount ~/.claude into the container.")] = False,
    mount_ssh: Annotated[bool, typer.Option("--mount-ssh", help="Mount ~/.ssh into the container.")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the generated overlay instead of writing it.")] = False,
) -> None:
    compose_path = file[0]
    compose = _load_yaml(compose_path)
    services = _service_names(compose)
    if not services:
        raise typer.BadParameter(f"no services found in {compose_path}")

    chosen = service or _pick_service(services)
    overlay = build_overlay(compose_path, chosen, openclaw_home, mount_bashrc, mount_codex, mount_claude, mount_ssh)
    rendered = yaml.safe_dump(overlay, sort_keys=False)

    if dry_run:
        typer.echo(rendered, nl=False)
    else:
        output.write_text(rendered, encoding="utf-8")
        typer.echo(f"Wrote {output}")


if __name__ == "__main__":
    app()
