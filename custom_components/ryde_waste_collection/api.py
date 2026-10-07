"""Ryde Council waste collection API helpers.

These helpers are Home Assistant-independent so they can be unit tested
without importing the HA runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from html import unescape
import logging
import re
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession, ClientTimeout

from .const import API_SEARCH_URL, API_WASTE_URL, WASTE_TYPES

_LOGGER = logging.getLogger(__name__)

# Akamai in front of ryde.nsw.gov.au returns 403 for several common
# User-Agent strings, including Home Assistant's default session header
# ("Home Assistant/...") and generic browser UAs. Per-request headers
# override the shared HA session so we can send an allowed value.
API_HEADERS = {
    "User-Agent": (
        "RydeWasteCollection/1.1.0 "
        "(+https://github.com/andrewkriley/ryde-waste-collection)"
    ),
    "Accept": "application/json",
}
REQUEST_TIMEOUT = ClientTimeout(total=10)

# "Tue 27/1/2026" or "Tue 27/01/2026"
_DATE_RE = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})")


class RydeApiError(Exception):
    """Base error for Ryde Council API failures."""


class AddressNotFoundError(RydeApiError):
    """No matching address was returned."""


class CannotConnectError(RydeApiError):
    """The Ryde Council API could not be reached or returned an error."""


@dataclass(frozen=True)
class AddressMatch:
    """A single address search result."""

    geolocation_id: str
    address: str
    score: float | None = None


@dataclass(frozen=True)
class WasteCollection:
    """Parsed next-collection information for one waste type."""

    date_text: str | None
    collection_date: date | None
    days_until: int | None


def extract_date(html_content: str, waste_type: str) -> str | None:
    """Extract the next-service date text for a waste type from council HTML."""
    pattern = (
        rf"<h3>{re.escape(waste_type)}</h3>.*?"
        r'<div class="next-service">\s*(.+?)\s*</div>'
    )
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def parse_collection_date(date_str: str) -> date | None:
    """Parse a council date string such as 'Tue 27/1/2026'."""
    if not date_str:
        return None
    match = _DATE_RE.search(date_str)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%d/%m/%Y").date()
    except ValueError:
        _LOGGER.warning("Error parsing date '%s'", date_str)
        return None


def calculate_days_until(collection: date, today: date) -> int:
    """Return whole days from today until the collection date."""
    return (collection - today).days


def parse_waste_schedule(html_content: str, today: date) -> dict[str, WasteCollection]:
    """Parse council waste HTML into a schedule keyed by waste type."""
    schedule: dict[str, WasteCollection] = {}
    for waste_type in WASTE_TYPES:
        date_text = extract_date(html_content, waste_type)
        collection_date = parse_collection_date(date_text) if date_text else None
        days_until = (
            calculate_days_until(collection_date, today) if collection_date else None
        )
        schedule[waste_type] = WasteCollection(
            date_text=date_text,
            collection_date=collection_date,
            days_until=days_until,
        )
    return schedule


def parse_address_matches(payload: dict[str, Any]) -> list[AddressMatch]:
    """Convert an address-search JSON payload into match objects."""
    matches: list[AddressMatch] = []
    for item in payload.get("Items") or []:
        geolocation_id = item.get("Id")
        address = item.get("AddressSingleLine")
        if not geolocation_id or not address:
            continue
        score = item.get("Score")
        matches.append(
            AddressMatch(
                geolocation_id=str(geolocation_id),
                address=str(address),
                score=float(score) if score is not None else None,
            )
        )
    return matches


async def async_search_addresses(
    session: ClientSession, keywords: str
) -> list[AddressMatch]:
    """Search Ryde Council for addresses matching keywords."""
    try:
        async with session.get(
            API_SEARCH_URL,
            params={"keywords": keywords},
            headers=API_HEADERS,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            response.raise_for_status()
            payload = await response.json()
    except (ClientError, TimeoutError, ValueError) as err:
        raise CannotConnectError(str(err)) from err

    matches = parse_address_matches(payload)
    if not matches:
        raise AddressNotFoundError(f"Address not found: {keywords}")
    return matches


async def async_fetch_waste_schedule(
    session: ClientSession, geolocation_id: str, today: date
) -> dict[str, WasteCollection]:
    """Fetch and parse the waste schedule for a geolocation ID."""
    try:
        async with session.get(
            API_WASTE_URL,
            params={"geolocationid": geolocation_id, "ocsvclang": "en-AU"},
            headers=API_HEADERS,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            response.raise_for_status()
            payload = await response.json()
    except ClientResponseError as err:
        raise CannotConnectError(str(err)) from err
    except (ClientError, TimeoutError, ValueError) as err:
        raise CannotConnectError(str(err)) from err

    if not payload.get("success"):
        raise RydeApiError("API returned success=false")

    html_content = unescape(payload.get("responseContent") or "")
    return parse_waste_schedule(html_content, today)
