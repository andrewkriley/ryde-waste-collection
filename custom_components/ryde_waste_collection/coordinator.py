"""DataUpdateCoordinator for Ryde Waste Collection."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    TimestampDataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import dt as dt_util

from .api import (
    AddressNotFoundError,
    CannotConnectError,
    RydeApiError,
    WasteCollection,
    async_fetch_waste_schedule,
    async_search_addresses,
)
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class RydeWasteCollectionCoordinator(
    TimestampDataUpdateCoordinator[dict[str, WasteCollection]]
):
    """Class to manage fetching Ryde waste collection data."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        geolocation_id: str | None = None,
        scan_interval: timedelta = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize."""
        self.address = address
        self.geolocation_id = geolocation_id
        self.normalized_address = address
        self._session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )

    async def _async_update_data(self) -> dict[str, WasteCollection]:
        """Fetch data from the Ryde Council API."""
        try:
            if not self.geolocation_id:
                matches = await async_search_addresses(self._session, self.address)
                match = matches[0]
                self.geolocation_id = match.geolocation_id
                self.normalized_address = match.address
                if len(matches) > 1:
                    _LOGGER.warning(
                        "Address %s matched %s results; using first result %s",
                        self.address,
                        len(matches),
                        match.address,
                    )
                else:
                    _LOGGER.info(
                        "Found address: %s (ID: %s)",
                        self.normalized_address,
                        self.geolocation_id,
                    )

            today = dt_util.now().date()
            return await async_fetch_waste_schedule(
                self._session, self.geolocation_id, today
            )
        except AddressNotFoundError as err:
            raise UpdateFailed(str(err)) from err
        except CannotConnectError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except RydeApiError as err:
            raise UpdateFailed(str(err)) from err
