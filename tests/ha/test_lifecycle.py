"""Run the integration through Home Assistant's real entry and timer lifecycle."""
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("homeassistant")

from homeassistant.config_entries import ConfigEntryState
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry, async_fire_time_changed,
)

DOMAIN = "ryde_waste_collection"
HTML = (Path(__file__).parents[1] / "fixtures/waste_response.html").read_text()

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def loaded_entry(hass, enable_custom_integrations, freezer, monkeypatch):
    """Use real sensors/coordinator, replacing only council network I/O."""
    import custom_components

    # The test helper ships a custom_components package; point it at this repo.
    monkeypatch.setattr(
        custom_components, "__path__",
        [str(Path(__file__).parents[2] / "custom_components")],
    )
    dt_util.set_default_time_zone(dt_util.get_time_zone("Australia/Sydney"))
    freezer.move_to("2026-08-24T13:59:50+00:00")  # 23:59:50 Sydney
    from custom_components.ryde_waste_collection.api import parse_waste_schedule

    async def fetch(_session, _geolocation_id, today):
        return parse_waste_schedule(HTML, today)

    entry = MockConfigEntry(
        domain=DOMAIN, title="Test address",
        data={"address": "Test address", "geolocation_id": "test-id"},
        options={"scan_interval": 24},
    )
    entry.add_to_hass(hass)
    with patch(
        "custom_components.ryde_waste_collection.coordinator.async_fetch_waste_schedule",
        side_effect=fetch,
    ) as fetch_mock:
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.state is ConfigEntryState.LOADED
        yield entry, fetch_mock
        if entry.state is ConfigEntryState.LOADED:
            assert await hass.config_entries.async_unload(entry.entry_id)
            await hass.async_block_till_done()


async def advance(hass, freezer, instant):
    freezer.move_to(instant)
    async_fire_time_changed(hass, datetime.fromisoformat(instant).astimezone(timezone.utc))
    await hass.async_block_till_done()


def bin_states(hass):
    return [s for s in hass.states.async_all("sensor") if "days_until" in s.attributes]


async def test_local_midnight_refresh_updates_sensor_days(hass, freezer, loaded_entry):
    _, fetch = loaded_entry
    assert sorted(s.attributes["days_until"] for s in bin_states(hass)) == [1, 1, 8]
    assert fetch.call_count == 1
    await advance(hass, freezer, "2026-08-24T13:59:59+00:00")
    assert fetch.call_count == 1
    await advance(hass, freezer, "2026-08-24T14:00:00+00:00")
    assert fetch.call_count == 2
    assert sorted(s.attributes["days_until"] for s in bin_states(hass)) == [0, 0, 7]


async def test_successful_unload_removes_data_sensors_and_midnight_timer(
    hass, freezer, loaded_entry,
):
    entry, fetch = loaded_entry
    entity_ids = [s.entity_id for s in bin_states(hass)]
    assert len(entity_ids) == 3
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED
    assert entry.entry_id not in hass.data[DOMAIN]
    # HA retains registered entities as unavailable placeholders after unload.
    assert all(
        hass.states.get(entity_id).state == "unavailable" for entity_id in entity_ids
    )
    assert not bin_states(hass)
    with patch.object(hass.config_entries, "async_reload") as reload_entry:
        hass.config_entries.async_update_entry(entry, options={"scan_interval": 12})
        await hass.async_block_till_done()
        reload_entry.assert_not_called()
    calls = fetch.call_count
    await advance(hass, freezer, "2026-08-24T14:00:00+00:00")
    await advance(hass, freezer, "2026-08-25T14:00:00+00:00")
    assert fetch.call_count == calls


async def test_failed_unload_keeps_data_and_midnight_timer(hass, freezer, loaded_entry):
    entry, fetch = loaded_entry
    coordinator = hass.data[DOMAIN][entry.entry_id]
    from custom_components.ryde_waste_collection import async_unload_entry

    with patch.object(hass.config_entries, "async_unload_platforms", return_value=False):
        assert not await async_unload_entry(hass, entry)
    assert hass.data[DOMAIN][entry.entry_id] is coordinator
    assert bin_states(hass)
    await advance(hass, freezer, "2026-08-24T14:00:00+00:00")
    assert fetch.call_count == 2


async def test_unload_then_setup_registers_only_one_midnight_refresh(
    hass, freezer, loaded_entry,
):
    entry, fetch = loaded_entry
    assert await hass.config_entries.async_unload(entry.entry_id)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    calls = fetch.call_count
    await advance(hass, freezer, "2026-08-24T14:00:00+00:00")
    assert fetch.call_count == calls + 1
    assert len(bin_states(hass)) == 3
