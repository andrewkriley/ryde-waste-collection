"""Config flow for Ryde Waste Collection integration."""
from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    API_SEARCH_URL,
    CONF_ADDRESS,
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


async def validate_address(hass: HomeAssistant, address: str) -> dict[str, Any]:
    """Validate the address by checking if it exists in Ryde Council's system."""
    params = {"keywords": address}

    try:
        response = await hass.async_add_executor_job(
            lambda: requests.get(API_SEARCH_URL, params=params, timeout=10)
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("Items") or len(data["Items"]) == 0:
            raise ValueError("address_not_found")

        # Return the normalized address
        return {
            "address": data["Items"][0]["AddressSingleLine"],
            "geolocation_id": data["Items"][0]["Id"],
        }

    except requests.exceptions.RequestException as err:
        _LOGGER.error("Error validating address: %s", err)
        raise ValueError("cannot_connect") from err


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ryde Waste Collection."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_address(self.hass, user_input[CONF_ADDRESS])

                # Set unique ID based on geolocation_id
                await self.async_set_unique_id(info["geolocation_id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["address"],
                    data={CONF_ADDRESS: user_input[CONF_ADDRESS]},
                )

            except ValueError as err:
                if str(err) == "address_not_found":
                    errors["base"] = "address_not_found"
                elif str(err) == "cannot_connect":
                    errors["base"] = "cannot_connect"
                else:
                    errors["base"] = "unknown"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Ryde Waste Collection."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

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
