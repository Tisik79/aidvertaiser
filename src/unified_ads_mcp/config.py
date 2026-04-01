"""Shared configuration helpers for Unified Ads MCP."""

from __future__ import annotations

import os
from pathlib import Path


_TRUTHY = {"1", "true", "yes", "y", "on"}

# Unified config directory — single source of truth for all credentials
CONFIG_DIR = Path.home() / ".unified-ads-mcp"


def resolve_config_path(filename: str, env_var: str | None = None) -> str:
    """Resolve config file path with unified fallback.

    Priority:
    1. Environment variable (if set and file exists)
    2. ~/.unified-ads-mcp/{filename}
    3. ~/{filename} (legacy fallback)
    """
    # 1. Env var override
    if env_var:
        env_path = os.environ.get(env_var)
        if env_path and os.path.exists(env_path):
            return env_path

    # 2. Unified config dir (preferred)
    unified_path = CONFIG_DIR / filename
    if unified_path.exists():
        return str(unified_path)

    # 3. Legacy home dir fallback
    legacy_path = Path.home() / filename
    if legacy_path.exists():
        return str(legacy_path)

    # Return unified path as default (even if doesn't exist yet)
    return str(unified_path)


def _env_flag(name: str) -> bool:
    value = os.environ.get(name)
    if value is None:
        return False
    return value.strip().lower() in _TRUTHY


def only_default_account_enabled() -> bool:
    """Return True when ONLY_DEFAULT_ACCOUNT is enabled via environment."""
    return _env_flag("ONLY_DEFAULT_ACCOUNT")
