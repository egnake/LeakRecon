"""Tests for core.tor_handler.TorHandler."""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from core.tor_handler import TorHandler


@pytest.fixture
def tor_handler():
    return TorHandler()


@pytest.mark.asyncio
async def test_get_returns_none_without_session(tor_handler):
    """Calling get() without an active session should return None."""
    result = await tor_handler.get("http://example.com")
    assert result is None


@pytest.mark.asyncio
async def test_verify_tor_connection_fail(tor_handler):
    """If connection fails, verify_tor_connection returns False."""
    with patch.object(tor_handler, "_create_session") as mock_session:
        mock_client = AsyncMock()
        mock_client.get = MagicMock(side_effect=Exception("Connection refused"))
        mock_client.close = AsyncMock()
        mock_session.return_value = mock_client
        result = await tor_handler.verify_tor_connection()
        assert result is False


@pytest.mark.asyncio
async def test_circuit_breaker_init(tor_handler):
    """Circuit breaker starts with no dead hosts."""
    dead = await tor_handler.get_dead_hosts()
    assert dead == []


@pytest.mark.asyncio
async def test_record_failure_and_dead_host(tor_handler):
    """Recording enough failures should mark a host as dead."""
    url = "http://deadhost.onion/test"
    # Record failures up to the threshold
    for _ in range(3):  # threshold is 2, so 2 failures => dead
        await tor_handler._record_failure(url)
    is_dead = await tor_handler.is_host_dead(url)
    assert is_dead is True


@pytest.mark.asyncio
async def test_record_success_clears_failure(tor_handler):
    """A successful request should clear the failure counter for that host."""
    url = "http://recovering.onion/test"
    await tor_handler._record_failure(url)
    await tor_handler._record_success(url)
    is_dead = await tor_handler.is_host_dead(url)
    assert is_dead is False


@pytest.mark.asyncio
async def test_reset_circuit_breaker(tor_handler):
    """Resetting the circuit breaker should clear all recorded failures."""
    await tor_handler._record_failure("http://host1.onion")
    await tor_handler._record_failure("http://host2.onion")
    await tor_handler.reset_circuit_breaker()
    dead = await tor_handler.get_dead_hosts()
    assert dead == []


@pytest.mark.asyncio
async def test_get_timeout_onion(tor_handler):
    """Onion URLs should use the ONION_TIMEOUT setting."""
    timeout = tor_handler._get_timeout("http://example.onion/page")
    assert timeout > 0  # Should be ONION_TIMEOUT from settings


@pytest.mark.asyncio
async def test_get_timeout_clearnet(tor_handler):
    """Clearnet URLs should use the CLEARNET_TIMEOUT setting."""
    timeout = tor_handler._get_timeout("http://example.com/page")
    assert timeout > 0  # Should be CLEARNET_TIMEOUT from settings


@pytest.mark.asyncio
async def test_get_timeout_explicit(tor_handler):
    """Explicit timeout should override default."""
    timeout = tor_handler._get_timeout("http://example.com", explicit_timeout=99)
    assert timeout == 99


@pytest.mark.asyncio
async def test_close_resets_state(tor_handler):
    """Closing the handler should reset session and IP."""
    tor_handler.session = MagicMock()
    tor_handler.session.close = AsyncMock()
    tor_handler.tor_ip = "1.2.3.4"
    await tor_handler.close()
    assert tor_handler.session is None
    assert tor_handler.tor_ip is None
