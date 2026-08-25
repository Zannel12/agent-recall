"""Pure, consent-gated Hermes MCP configuration planning.

This module only constructs a reviewable plan. It does not inspect or mutate
Hermes configuration, invoke a subprocess, or start an MCP server.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


SERVER_NAME = "agent-recall"


class PlanStatus(str, Enum):
    READY = "ready"
    CONSENT_REQUIRED = "consent_required"
    CONFIG_MISSING = "config_missing"
    NAME_COLLISION = "name_collision"
    INVALID_BACKUP = "invalid_backup"


@dataclass(frozen=True)
class HermesMcpPlan:
    status: PlanStatus
    config_entry: dict[str, object]
    commands: tuple[tuple[str, ...], ...]
    cli_fallback: tuple[str, ...]


def _config_entry(vault_path: Path) -> dict[str, object]:
    return {
        "command": "agent-recall-mcp",
        "args": ["--vault", str(vault_path)],
        "tools": {"include": ["search"]},
        "sampling": {"enabled": False},
    }


def build_hermes_mcp_plan(
    *,
    config_path: Path,
    backup_path: Path,
    vault_path: Path,
    observed_server_names: set[str],
    config_exists: bool,
    consent: bool,
) -> HermesMcpPlan:
    """Return a non-executing plan from explicit caller-provided observations."""
    fallback = ("agent-recall", "search", "--vault", str(vault_path))
    entry = _config_entry(vault_path)
    if not consent:
        return HermesMcpPlan(PlanStatus.CONSENT_REQUIRED, entry, (), fallback)
    if not config_exists:
        return HermesMcpPlan(PlanStatus.CONFIG_MISSING, entry, (), fallback)
    if config_path == backup_path:
        return HermesMcpPlan(PlanStatus.INVALID_BACKUP, entry, (), fallback)
    if SERVER_NAME in observed_server_names:
        return HermesMcpPlan(PlanStatus.NAME_COLLISION, entry, (), fallback)

    commands = (
        ("cp", "--", str(config_path), str(backup_path)),
        (
            "hermes",
            "mcp",
            "add",
            SERVER_NAME,
            "--command",
            "agent-recall-mcp",
            "--args",
            "--vault",
            str(vault_path),
        ),
        ("hermes", "mcp", "configure", SERVER_NAME),
        ("hermes", "mcp", "remove", SERVER_NAME),
    )
    return HermesMcpPlan(PlanStatus.READY, entry, commands, fallback)
