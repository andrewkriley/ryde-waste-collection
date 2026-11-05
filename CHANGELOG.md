# Changelog

## 1.1.2

Patch release for collection schedule reliability; no new public features or breaking changes.

- Refresh collection countdowns at local midnight
- Parse nested council HTML without assigning another bin's collection date
- Reject malformed or empty API responses; mark bins without valid dates unavailable
- Expand API and Home Assistant lifecycle regression tests
- Harden CI permissions, action revisions and dependency audits
- Validate live council address search and all three bin dates
- Keep the manifest and API User-Agent at `1.1.2`

## 1.1.1

Consumer README for the live HACS default-store listing.

- HACS search is the recommended install path
- Custom repository install is only for testing a branch that is not the published release
- User-Agent reports `RydeWasteCollection/1.1.1`

## 1.1.0

First HACS-ready release. Requires Home Assistant 2026.3 or later.

- Brand icons in `custom_components/ryde_waste_collection/brand/` for Home Assistant 2026.3+ local brands
- aiohttp client with a WAF-safe User-Agent for Ryde Council APIs
- Address search always asks for confirmation when a match is found
- Sensors use `TimestampDataUpdateCoordinator`, `DeviceInfo`, and omit `days_until` when the date cannot be parsed
- GitHub Actions: HACS validation, hassfest, and unit tests
