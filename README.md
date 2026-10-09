# Ryde Waste Collection

<p align="center">
  <img src="https://github.com/andrewkriley/ryde-waste-collection/raw/main/brand/icon.png" alt="Ryde Waste Collection" width="160" height="160">
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/andrewkriley/ryde-waste-collection.svg?style=flat-square)](LICENSE)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andrewkriley&repository=ryde-waste-collection&category=integration)

Unofficial Home Assistant integration for City of Ryde waste collection schedules.

Created by Andrew Riley. Not affiliated with or endorsed by the City of Ryde Council.

Current release: **1.1.0**. Requires **Home Assistant 2026.3 or later** so the integration can ship its own brand icon. It is intended for current Home Assistant 2026.10 installs.

## Features

- Next collection dates for general waste, recycling, and garden organics
- Days-until attributes for automations and dashboard colours
- UI setup with address search and a picker when several matches are found
- Configurable poll interval (1–24 hours)
- Multiple addresses via separate config entries

## Installation

### HACS custom repository (recommended)

This integration is not yet in the default HACS store. Add it as a custom repository:

1. [Open the repository in HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=andrewkriley&repository=ryde-waste-collection&category=integration), or in HACS go to **⋯ → Custom repositories**
2. Repository: `https://github.com/andrewkriley/ryde-waste-collection`
3. Category: **Integration**
4. Download the integration and restart Home Assistant

HACS will hide the download if the Home Assistant instance is older than 2026.3.0.

### Manual installation

Copy only the integration folder into Home Assistant:

```bash
git clone https://github.com/andrewkriley/ryde-waste-collection.git
cp -R ryde-waste-collection/custom_components/ryde_waste_collection \
  /path/to/homeassistant/custom_components/ryde_waste_collection
```

Do not clone the whole repository into `custom_components/ryde_waste_collection`. The integration files live one directory deeper.

Restart Home Assistant after copying.

## Configuration

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **Ryde Waste Collection**
4. Enter a City of Ryde address, for example `128 Blaxland Road Ryde 2112` (do not include `NSW`)
5. Confirm the matched address, or choose the correct one if several are listed

The integration is unofficial. Dates come from Ryde Council public APIs and should be confirmed on the [council website](https://www.ryde.nsw.gov.au/) if you need official information.

## Brand icon

Home Assistant 2026.3+ serves icons from `custom_components/ryde_waste_collection/brand/`. After install, **Settings → Devices & services → Add Integration** and the integration device page show the Ryde Waste bins logo.

The HACS downloads panel may still show “icon not available” until HACS uses the local brands API ([hacs/integration#5223](https://github.com/hacs/integration/issues/5223)). That is a HACS frontend issue, not a missing file in this repository.

Do not open a `home-assistant/brands` PR for this custom integration. That repository now auto-closes `custom_integrations/*` submissions and points authors at the local `brand/` directory.

## Sensor entities

Each config entry creates three sensors:

| Entity | Meaning |
| --- | --- |
| `sensor.ryde_waste_collection_general_waste` | Next red-bin collection |
| `sensor.ryde_waste_collection_recycling` | Next yellow-bin collection |
| `sensor.ryde_waste_collection_garden_organics` | Next green-bin collection |

State is the council display string, for example `Tue 25/8/2026`.

Attributes:

- `days_until` — whole days until collection. Omitted when the date cannot be parsed
- `collection_date` / `next_collection` — same display string as the state
- `collection_date_iso` — `YYYY-MM-DD` when parsing succeeds
- `address` — normalized Ryde Council address
- `geolocation_id` — council location id used for schedule lookups
- `last_updated` — timestamp of the last successful coordinator refresh

## Customization

See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for Mushroom and button-card examples that colour icons when collection is within 7 days.

If Mushroom templates do not apply colours, see [docs/TROUBLESHOOTING_COLORS.md](docs/TROUBLESHOOTING_COLORS.md).

## Documentation

- [Customization](docs/CUSTOMIZATION.md)
- [API notes](docs/API_VALIDATION.md)
- [Contributing](CONTRIBUTING.md)

## Development

```
ryde-waste-collection/
├── custom_components/ryde_waste_collection/
│   ├── __init__.py
│   ├── api.py
│   ├── config_flow.py
│   ├── coordinator.py
│   ├── sensor.py
│   ├── const.py
│   ├── manifest.json
│   ├── strings.json
│   └── translations/
│   └── brand/               # HACS brand assets
├── tests/
├── docs/
├── hacs.json
└── .github/workflows/
```

Link the integration directory, not the repository root:

```bash
ln -s /path/to/ryde-waste-collection/custom_components/ryde_waste_collection \
  /path/to/homeassistant/custom_components/ryde_waste_collection
```

Run unit tests:

```bash
pip install pytest aiohttp
pytest -q
```

## HACS default-store status

Release **1.1.0** is the version HACS should download (`manifest.json` `version` and the GitHub Release tag match).

Remaining owner step for the default store:

1. Open a PR against [hacs/default](https://github.com/hacs/default) adding `andrewkriley/ryde-waste-collection` alphabetically to `./integration`

## License

MIT. See [LICENSE](LICENSE).

## Credits

- Author: Andrew Riley
- Inspired by the Ryde source in [mampfes/hacs_waste_collection_schedule](https://github.com/mampfes/hacs_waste_collection_schedule/blob/master/doc/source/ryde_nsw_gov_au.md)
- Data: City of Ryde public APIs
