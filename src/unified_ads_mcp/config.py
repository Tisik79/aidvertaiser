"""Shared configuration helpers for Unified Ads MCP."""

from __future__ import annotations

import os


_TRUTHY = {"1", "true", "yes", "y", "on"}


def _env_flag(name: str) -> bool:
    value = os.environ.get(name)
    if value is None:
        return False
    return value.strip().lower() in _TRUTHY


def only_default_account_enabled() -> bool:
    """Return True when ONLY_DEFAULT_ACCOUNT is enabled via environment."""
    return _env_flag("ONLY_DEFAULT_ACCOUNT")
