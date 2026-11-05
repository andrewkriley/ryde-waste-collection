"""Exercise request handling without contacting the council."""
import asyncio
from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientConnectionError

from ryde_waste_collection.api import (
    API_HEADERS, REQUEST_TIMEOUT, AddressNotFoundError, CannotConnectError,
    RydeApiError, async_fetch_waste_schedule, async_search_addresses,
)

TODAY = date(2026, 8, 24)
HTML = '<h3>General Waste</h3><div class="next-service">Tue 25/8/2026</div>'


def session_for(payload=None, error=None):
    response = MagicMock()
    response.json = AsyncMock(return_value=payload)
    response.raise_for_status.side_effect = error
    session = MagicMock()
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=False)
    return session


def test_fetch_request_and_partial_schedule():
    session = session_for({"success": True, "responseContent": HTML})
    result = asyncio.run(async_fetch_waste_schedule(session, "geo-id", TODAY))
    assert result["General Waste"].days_until == 1
    assert result["Recycling"].collection_date is None
    kwargs = session.get.call_args.kwargs
    assert kwargs["params"]["geolocationid"] == "geo-id"
    assert kwargs["headers"] == API_HEADERS
    assert kwargs["timeout"] == REQUEST_TIMEOUT


@pytest.mark.parametrize("payload", [
    None, [], {"success": False}, {"success": "false", "responseContent": HTML},
    {"success": True}, {"success": True, "responseContent": 123},
    {"success": True, "responseContent": ""},
    {"success": True, "responseContent": "<p>No collections</p>"},
])
def test_fetch_rejects_invalid_responses(payload):
    with pytest.raises(RydeApiError):
        asyncio.run(async_fetch_waste_schedule(session_for(payload), "id", TODAY))


@pytest.mark.parametrize("operation", ["search", "schedule"])
@pytest.mark.parametrize("error", [ClientConnectionError("offline"), TimeoutError(), ValueError("invalid JSON")])
def test_request_errors_are_normalized(operation, error):
    session = session_for()
    session.get.return_value.__aenter__.side_effect = error
    with pytest.raises(CannotConnectError):
        asyncio.run(
            async_search_addresses(session, "address") if operation == "search"
            else async_fetch_waste_schedule(session, "id", TODAY)
        )


def test_search_empty_results():
    with pytest.raises(AddressNotFoundError):
        asyncio.run(async_search_addresses(session_for({"Items": []}), "address"))


@pytest.mark.parametrize("payload", [None, [], {}, {"Items": "invalid"}])
def test_search_invalid_payload(payload):
    with pytest.raises(RydeApiError):
        asyncio.run(async_search_addresses(session_for(payload), "address"))
