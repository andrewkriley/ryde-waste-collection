"""Ryde Council waste collection API helpers.

These helpers are Home Assistant-independent so they can be unit tested
without importing the HA runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from html import unescape
from html.parser import HTMLParser
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
        "RydeWasteCollection/1.1.2 "
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


class _ScheduleParser(HTMLParser):
    """Read heading and service text without crossing into another bin section."""

    def __init__(self) -> None:
        super().__init__()
        self.dates: dict[str, str] = {}
        self.heading: list[str] | None = None
        self.waste_type: str | None = None
        self.service: list[str] | None = None
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h3":
            self.heading = []
            self.waste_type = None
            self.service = None
            self.depth = 0
        if self.service is not None and tag == "div":
            self.depth += 1
        elif tag == "div" and self.waste_type:
            classes = (dict(attrs).get("class") or "").split()
            if "next-service" in classes:
                self.service = []
                self.depth = 1

    def handle_data(self, data: str) -> None:
        if self.heading is not None:
            self.heading.append(data)
        if self.service is not None:
            self.service.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h3" and self.heading is not None:
            heading = " ".join("".join(self.heading).split()).casefold()
            self.waste_type = next(
                (kind for kind in WASTE_TYPES if kind.casefold() == heading), None
            )
            self.heading = None
        if tag == "div" and self.service is not None:
            self.depth -= 1
            if self.depth == 0:
                text = " ".join("".join(self.service).split())
                if text and self.waste_type:
                    self.dates.setdefault(self.waste_type, text)
                self.service = None


def extract_date(html_content: str, waste_type: str) -> str | None:
    """Extract visible next-service text for exactly one waste heading."""
    parser = _ScheduleParser()
    parser.feed(html_content)
    return parser.dates.get(waste_type)


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
    if not isinstance(payload, dict) or not isinstance(payload.get("Items"), list):
        raise RydeApiError("Invalid address search response")
    matches: list[AddressMatch] = []
    for item in payload["Items"]:
        if not isinstance(item, dict):
            continue
        geolocation_id = item.get("Id")
        address = item.get("AddressSingleLine")
        if not geolocation_id or not address:
            continue
        score = item.get("Score")
        try:
            score = float(score) if score is not None else None
        except (TypeError, ValueError):
            score = None
        matches.append(
            AddressMatch(
                geolocation_id=str(geolocation_id),
                address=str(address),
                score=score,
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

    if not isinstance(payload, dict):
        raise RydeApiError("Invalid waste schedule response")
    if payload.get("success") is not True:
        raise RydeApiError("API returned success=false")

    content = payload.get("responseContent")
    if not isinstance(content, str):
        raise RydeApiError("Invalid waste schedule HTML")
    html_content = unescape(content)
    schedule = parse_waste_schedule(html_content, today)
    if not any(item.collection_date is not None for item in schedule.values()):
        raise RydeApiError("Council response contained no valid collection dates")
    return schedule
