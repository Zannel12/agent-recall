"""Pure, caller-supplied capability negotiation for bounded adapters."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar


class TransportMode(str, Enum):
    NATIVE_PROVIDER = "native_provider"
    MCP = "mcp"
    CLI = "cli"


class RetrievalMode(str, Enum):
    HYBRID = "hybrid"
    SPARSE = "sparse"
    LEXICAL = "lexical"


Mode = TypeVar("Mode", bound=Enum)


@dataclass(frozen=True)
class CapabilityChoice(Generic[Mode]):
    selected: Mode | None
    available: bool
    degraded: bool
    reason: str | None


def _choose(available_modes: set[Mode], priority: tuple[Mode, ...], unavailable_reason: str) -> CapabilityChoice[Mode]:
    selected = next((mode for mode in priority if mode in available_modes), None)
    if selected is None:
        return CapabilityChoice(
            selected=None,
            available=False,
            degraded=False,
            reason=unavailable_reason,
        )

    unavailable = [mode.value for mode in priority[: priority.index(selected)] if mode not in available_modes]
    return CapabilityChoice(
        selected=selected,
        available=True,
        degraded=bool(unavailable),
        reason=",".join(f"{mode}_unavailable" for mode in unavailable) or None,
    )


def choose_transport_mode(available_modes: set[TransportMode]) -> CapabilityChoice[TransportMode]:
    """Choose from explicit caller-supplied modes without detecting or invoking a host."""
    return _choose(
        available_modes,
        (TransportMode.NATIVE_PROVIDER, TransportMode.MCP, TransportMode.CLI),
        "no_transport_available",
    )


def choose_retrieval_mode(available_modes: set[RetrievalMode]) -> CapabilityChoice[RetrievalMode]:
    """Choose an explicit retrieval mode without loading models or executing retrieval."""
    return _choose(
        available_modes,
        (RetrievalMode.HYBRID, RetrievalMode.SPARSE, RetrievalMode.LEXICAL),
        "no_retrieval_mode_available",
    )
