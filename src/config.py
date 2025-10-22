"""Configuration module for DrinkGame application."""
import os
from typing import Final


def _get_bool_env(key: str, default: bool) -> bool:
    """Get boolean environment variable."""
    return bool(int(os.getenv(key, str(int(default)))))


def _get_int_env(key: str, default: int) -> int:
    """Get integer environment variable."""
    return int(os.getenv(key, str(default)))


def _get_str_env(key: str, default: str) -> str:
    """Get string environment variable."""
    return os.getenv(key, default)


# Application settings
DEBUG: Final[bool] = _get_bool_env("DEBUG", True)

# Lobby settings
INACTIVE_LOBBY_TIME: Final[int] = _get_int_env("INACTIVE_LOBBY_TIME", 3600)  # 1 Hour
CODE_LEN: Final[int] = _get_int_env("CODE_LEN", 5)

# WebSocket settings
WEB_SOCKET_URL: Final[str] = _get_str_env("WEB_SOCKET_URL", "http://192.168.91.200:5000/")