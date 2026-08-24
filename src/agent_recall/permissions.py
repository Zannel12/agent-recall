from __future__ import annotations

from enum import StrEnum


class NamespaceScope(StrEnum):
    USER = "user"
    AGENT = "agent"
    PROJECT = "project"
    TASK = "task"


class Action(StrEnum):
    READ = "read"
    WRITE = "write"


_READ_ONLY_ALLOWLIST = frozenset((scope, Action.READ) for scope in NamespaceScope)


def is_allowed(scope: object, action: object) -> bool:
    """Evaluate a closed, category-only capability gate without executing I/O."""
    if not isinstance(scope, NamespaceScope) or not isinstance(action, Action):
        return False
    return (scope, action) in _READ_ONLY_ALLOWLIST
