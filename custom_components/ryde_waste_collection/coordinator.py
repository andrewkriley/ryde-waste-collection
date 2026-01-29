"""DataUpdateCoordinator for Ryde Waste Collection."""
from datetime import datetime, timedelta
import logging
import re
from html import unescape

import requests
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_SEARCH_URL,
    API_WASTE_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    WASTE_TYPE_GENERAL,
    WASTE_TYPE_RECYCLING,
    WASTE_TYPE_GARDEN,
)

_LOGGER = logging.getLogger(__name__)


class RydeWasteCollectionCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ryde waste collection data."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        scan_interval: timedelta = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize."""
        self.address = address
        self.geolocation_id = None
        self.normalized_address = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # Search for address if we don't have geolocation_id yet
            if not self.geolocation_id:
                await self._async_search_address()

            # Fetch waste schedule
            return await self._async_fetch_waste_schedule()

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _async_search_address(self):
        """Search for address and get geolocation ID."""
        params = {"keywords": self.address}

        try:
            response = await self.hass.async_add_executor_job(
                lambda: requests.get(API_SEARCH_URL, params=params, timeout=10)
            )
            response.raise_for_status()
            data = response.json()

            if data.get("Items") and len(data["Items"]) > 0:
                first_result = data["Items"][0]
                self.geolocation_id = first_result["Id"]
                self.normalized_address = first_result["AddressSingleLine"]
                _LOGGER.info(
                    "Found address: %s (ID: %s)",
                    self.normalized_address,
                    self.geolocation_id,
                )
            else:
                raise UpdateFailed(f"Address not found: {self.address}")

        except requests.exceptions.RequestException as err:
            raise UpdateFailed(f"Error searching for address: {err}") from err

    async def _async_fetch_waste_schedule(self):
        """Fetch waste collection schedule."""
        params = {"geolocationid": self.geolocation_id, "ocsvclang": "en-AU"}

        try:
            response = await self.hass.async_add_executor_job(
                lambda: requests.get(API_WASTE_URL, params=params, timeout=10)
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                raise UpdateFailed("API returned success=false")

            # Parse HTML content
            html_content = unescape(data["responseContent"])
            schedule = {}

            # Extract dates for each waste type
            schedule[WASTE_TYPE_GENERAL] = self._extract_date(
                html_content, "General Waste"
            )
            schedule[WASTE_TYPE_GARDEN] = self._extract_date(
                html_content, "Garden Organics"
            )
            schedule[WASTE_TYPE_RECYCLING] = self._extract_date(html_content, "Recycling")

            # Calculate days until collection for each type
            for waste_type, date_str in schedule.items():
                if date_str:
                    schedule[waste_type] = {
                        "date": date_str,
                        "days_until": self._calculate_days_until(date_str),
                    }

            return schedule

        except requests.exceptions.RequestException as err:
            raise UpdateFailed(f"Error fetching waste schedule: {err}") from err

    def _extract_date(self, html_content: str, waste_type: str) -> str | None:
        """Extract collection date from HTML for a specific waste type."""
        pattern = (
            rf'<h3>{waste_type}</h3>.*?<div class="next-service">\s*(.+?)\s*</div>'
        )
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _calculate_days_until(self, date_str: str) -> int:
        """Calculate days until collection date."""
        try:
            # Parse date string like "Tue 27/1/2026"
            date_parts = date_str.split()
            if len(date_parts) >= 2:
                date_obj = datetime.strptime(date_parts[1], "%d/%m/%Y").date()
                today = datetime.now().date()
                delta = (date_obj - today).days
                return delta
        except (ValueError, IndexError) as err:
            _LOGGER.warning("Error parsing date '%s': %s", date_str, err)
        return 0
