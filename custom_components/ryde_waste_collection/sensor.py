"""Sensor platform for Ryde Waste Collection."""
from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_ADDRESS,
    ATTR_COLLECTION_DATE,
    ATTR_DAYS_UNTIL,
    ATTR_GEOLOCATION_ID,
    ATTR_LAST_UPDATED,
    ATTR_NEXT_COLLECTION,
    DOMAIN,
    SENSOR_TYPES,
    WASTE_TYPES,
)
from .coordinator import RydeWasteCollectionCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Ryde Waste Collection sensors."""
    coordinator: RydeWasteCollectionCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for waste_type in WASTE_TYPES:
        entities.append(RydeWasteCollectionSensor(coordinator, entry, waste_type))

    async_add_entities(entities)


class RydeWasteCollectionSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Ryde Waste Collection sensor."""

    def __init__(
        self,
        coordinator: RydeWasteCollectionCoordinator,
        entry: ConfigEntry,
        waste_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.waste_type = waste_type
        self._attr_has_entity_name = True

        sensor_info = SENSOR_TYPES[waste_type]

        # Set unique ID
        self._attr_unique_id = (
            f"{entry.entry_id}_{sensor_info['key']}"
        )

        # Set entity name and icon
        self._attr_name = sensor_info["name"]
        self._attr_icon = sensor_info["icon"]

        # Device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Ryde Waste Collection",
            "manufacturer": "Ryde Council",
            "model": "Waste Collection Schedule",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.coordinator.data and self.waste_type in self.coordinator.data:
            data = self.coordinator.data[self.waste_type]
            if data and "date" in data:
                return data["date"]
        return None

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes."""
        attributes = {
            ATTR_ADDRESS: self.coordinator.normalized_address or self.coordinator.address,
            ATTR_GEOLOCATION_ID: self.coordinator.geolocation_id,
            ATTR_LAST_UPDATED: datetime.now().isoformat(),
        }

        if self.coordinator.data and self.waste_type in self.coordinator.data:
            data = self.coordinator.data[self.waste_type]
            if data:
                if "date" in data:
                    attributes[ATTR_COLLECTION_DATE] = data["date"]
                    attributes[ATTR_NEXT_COLLECTION] = data["date"]
                if "days_until" in data:
                    attributes[ATTR_DAYS_UNTIL] = data["days_until"]

        return attributes

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self.waste_type in self.coordinator.data
        )
