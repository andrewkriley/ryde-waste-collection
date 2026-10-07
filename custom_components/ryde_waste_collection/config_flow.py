"""Config flow for Ryde Waste Collection integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .api import (
    AddressMatch,
    AddressNotFoundError,
    CannotConnectError,
    RydeApiError,
    async_search_addresses,
)
from .const import (
    CONF_ADDRESS,
    CONF_GEOLOCATION_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADDRESS): cv.string,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ryde Waste Collection."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the flow."""
        self._matches: list[AddressMatch] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial address search step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            try:
                self._matches = await async_search_addresses(
                    session, user_input[CONF_ADDRESS]
                )
            except AddressNotFoundError:
                errors["base"] = "address_not_found"
            except CannotConnectError:
                errors["base"] = "cannot_connect"
            except RydeApiError:
                _LOGGER.exception("Unexpected Ryde API error")
                errors["base"] = "unknown"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                if len(self._matches) == 1:
                    return await self._async_create_from_match(self._matches[0])
                return await self.async_step_select_address()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_select_address(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Let the user pick the correct address when search is ambiguous."""
        if user_input is not None:
            selected_id = user_input[CONF_GEOLOCATION_ID]
            for match in self._matches:
                if match.geolocation_id == selected_id:
                    return await self._async_create_from_match(match)
            return self.async_abort(reason="unknown")

        options = {
            match.geolocation_id: match.address for match in self._matches
        }
        return self.async_show_form(
            step_id="select_address",
            data_schema=vol.Schema(
                {vol.Required(CONF_GEOLOCATION_ID): vol.In(options)}
            ),
        )

    async def _async_create_from_match(self, match: AddressMatch) -> FlowResult:
        """Create a config entry for a confirmed address match."""
        await self.async_set_unique_id(match.geolocation_id)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=match.address,
            data={
                CONF_ADDRESS: match.address,
                CONF_GEOLOCATION_ID: match.geolocation_id,
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Ryde Waste Collection."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL,
                            DEFAULT_SCAN_INTERVAL.total_seconds() / 3600,
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=1, max=24)),
                }
            ),
        )
