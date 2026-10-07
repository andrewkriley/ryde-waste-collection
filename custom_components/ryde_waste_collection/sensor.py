"""Sensor platform for Ryde Waste Collection."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import WasteCollection
from .const import (
    ATTR_ADDRESS,
    ATTR_COLLECTION_DATE,
    ATTR_DAYS_UNTIL,
    ATTR_GEOLOCATION_ID,
    ATTR_LAST_UPDATED,
    ATTR_NEXT_COLLECTION,
    DEFAULT_NAME,
    DOMAIN,
    SENSOR_TYPES,
    WASTE_TYPES,
)
from .coordinator import RydeWasteCollectionCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Ryde Waste Collection sensors."""
    coordinator: RydeWasteCollectionCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        RydeWasteCollectionSensor(coordinator, entry, waste_type)
        for waste_type in WASTE_TYPES
    )


class RydeWasteCollectionSensor(CoordinatorEntity[RydeWasteCollectionCoordinator], SensorEntity):
    """Representation of a Ryde Waste Collection sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RydeWasteCollectionCoordinator,
        entry: ConfigEntry,
        waste_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.waste_type = waste_type
        sensor_info = SENSOR_TYPES[waste_type]
        self._attr_unique_id = f"{entry.entry_id}_{sensor_info['key']}"
        self._attr_name = sensor_info["name"]
        self._attr_icon = sensor_info["icon"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=coordinator.normalized_address or DEFAULT_NAME,
            manufacturer="City of Ryde",
            model="Waste collection schedule",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="https://www.ryde.nsw.gov.au/",
        )

    def _waste_data(self) -> WasteCollection | None:
        """Return parsed data for this waste type."""
        if not self.coordinator.data:
            return None
        data = self.coordinator.data.get(self.waste_type)
        if isinstance(data, WasteCollection):
            return data
        return None

    @property
    def native_value(self) -> str | None:
        """Return the next collection date as shown by Ryde Council."""
        data = self._waste_data()
        if data and data.date_text:
            return data.date_text
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        last_updated = None
        if self.coordinator.last_update_success_time is not None:
            last_updated = self.coordinator.last_update_success_time.isoformat()

        attributes: dict[str, Any] = {
            ATTR_ADDRESS: self.coordinator.normalized_address or self.coordinator.address,
            ATTR_GEOLOCATION_ID: self.coordinator.geolocation_id,
            ATTR_LAST_UPDATED: last_updated,
        }

        data = self._waste_data()
        if data:
            if data.date_text:
                attributes[ATTR_COLLECTION_DATE] = data.date_text
                attributes[ATTR_NEXT_COLLECTION] = data.date_text
            if data.collection_date is not None:
                attributes["collection_date_iso"] = data.collection_date.isoformat()
            if data.days_until is not None:
                attributes[ATTR_DAYS_UNTIL] = data.days_until

        return attributes

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self._waste_data() is not None
