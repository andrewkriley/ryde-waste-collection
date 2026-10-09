# Ryde Waste Collection

<p align="center">
  <img src="https://github.com/andrewkriley/ryde-waste-collection/raw/main/brand/icon.png" alt="Ryde Waste Collection" width="160" height="160">
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/andrewkriley/ryde-waste-collection.svg?style=flat-square)](LICENSE)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andrewkriley&repository=ryde-waste-collection&category=integration)

Unofficial Home Assistant integration for City of Ryde waste collection schedules.

Created by Andrew Riley. Not affiliated with or endorsed by the City of Ryde Council.

Requires **Home Assistant 2026.3 or later**. Current release: **1.1.0**.

## Features

- Next collection dates for general waste, recycling, and garden organics
- Days-until attributes for automations and dashboard colours
- UI setup with address search
- Configurable poll interval (1–24 hours)
- Multiple addresses via separate config entries

## Installation

### HACS (recommended)

1. Open **HACS** in Home Assistant
2. Search for **Ryde Waste Collection**
3. Download the integration and restart Home Assistant

If it does not appear in search yet, add it as a custom repository (below) until the [default-store listing](https://github.com/hacs/default/pull/11716) is merged.

### Custom repository (optional)

Use this to install before the default-store listing is live, or to test a branch that is not the published release.

1. In HACS go to **⋯ → Custom repositories**, or [open this repository in HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=andrewkriley&repository=ryde-waste-collection&category=integration)
2. Repository: `https://github.com/andrewkriley/ryde-waste-collection`
3. Category: **Integration**
4. Download the release or branch you want, then restart Home Assistant

## Configuration

1. Go to **Settings → Devices & services**
2. Click **+ Add Integration**
3. Search for **Ryde Waste Collection**
4. Enter a City of Ryde address, for example `128 Blaxland Road Ryde 2112` (do not include `NSW`)
5. Confirm the matched address, or choose the correct one if several are listed

Dates come from Ryde Council public APIs. Confirm them on the [council website](https://www.ryde.nsw.gov.au/) if you need official information.

## Sensors

Each address creates three sensors:

| Sensor | Meaning |
| --- | --- |
| General waste | Next red-bin collection |
| Recycling | Next yellow-bin collection |
| Garden organics | Next green-bin collection |

State is the council display string, for example `Tue 25/8/2026`.

Useful attributes:

- `days_until` — whole days until collection (omitted if the date cannot be parsed)
- `collection_date` — same display string as the state
- `collection_date_iso` — `YYYY-MM-DD` when parsing succeeds
- `address` — normalized Ryde Council address

## Dashboard colours

See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for Mushroom and button-card examples that colour icons when collection is within 7 days.

If colours do not apply, see [docs/TROUBLESHOOTING_COLORS.md](docs/TROUBLESHOOTING_COLORS.md).

## License

MIT. See [LICENSE](LICENSE).
