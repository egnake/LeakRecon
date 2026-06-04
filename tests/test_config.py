"""Tests for config.py Settings class."""
import os
import pytest
from unittest.mock import patch


def _clean_env():
    """Returns a copy of os.environ without any LeakRecon settings keys."""
    keys_to_strip = {
        "TOR_PROXY_HOST", "TOR_PROXY_PORT",
        "ONION_TIMEOUT", "CLEARNET_TIMEOUT",
        "MAX_RETRIES", "RETRY_BACKOFF",
        "CIRCUIT_BREAKER_THRESHOLD", "MAX_CONCURRENCY",
        "USER_AGENT", "TOR_CHECK_URL",
    }
    return {k: v for k, v in os.environ.items() if k not in keys_to_strip}


def _make_settings(**overrides):
    """Create a Settings instance with a clean environment (no .env contamination)."""
    clean = _clean_env()
    clean.update({k.upper(): str(v) for k, v in overrides.items()})
    with patch.dict(os.environ, clean, clear=True):
        # Re-import to bypass cached module state
        from config import Settings
        return Settings(_env_file=None, **overrides)


def test_settings_code_defaults():
    """Verify that the code-level defaults (config.py) are loaded correctly
    when no .env file and no environment overrides are present."""
    settings = _make_settings()
    assert settings.TOR_PROXY_HOST == "torproxy"
    assert settings.TOR_PROXY_PORT == 9050
    assert settings.MAX_CONCURRENCY == 25
    assert settings.ONION_TIMEOUT == 20
    assert settings.CLEARNET_TIMEOUT == 10
    assert settings.MAX_RETRIES == 2
    assert settings.RETRY_BACKOFF == 2.0
    assert settings.CIRCUIT_BREAKER_THRESHOLD == 2


def test_tor_proxy_url_default():
    """Verify the constructed SOCKS5 proxy URL from code defaults."""
    settings = _make_settings()
    assert settings.tor_proxy_url == "socks5://torproxy:9050"


def test_custom_port():
    """Verify that an explicit port override is reflected."""
    settings = _make_settings(TOR_PROXY_PORT=9150)
    assert settings.TOR_PROXY_PORT == 9150
    assert "9150" in settings.tor_proxy_url


def test_custom_host_and_port():
    """Verify that custom host and port are reflected in the proxy URL."""
    settings = _make_settings(TOR_PROXY_HOST="127.0.0.1", TOR_PROXY_PORT=9050)
    assert settings.tor_proxy_url == "socks5://127.0.0.1:9050"


def test_user_agent_default():
    """Verify the default User-Agent string contains expected fragments."""
    settings = _make_settings()
    assert "Mozilla/5.0" in settings.USER_AGENT
    assert "Chrome" in settings.USER_AGENT


def test_tor_check_url_default():
    """Verify the default Tor check URL."""
    settings = _make_settings()
    assert settings.TOR_CHECK_URL == "https://check.torproject.org/api/ip"
