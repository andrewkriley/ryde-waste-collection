# Changelog

## 1.1.0

First HACS-ready release. Requires Home Assistant 2026.3 or later.

- Brand icons in `custom_components/ryde_waste_collection/brand/` for Home Assistant 2026.3+ local brands
- aiohttp client with a WAF-safe User-Agent for Ryde Council APIs
- Address search always asks for confirmation when a match is found
- Sensors use `TimestampDataUpdateCoordinator`, `DeviceInfo`, and omit `days_until` when the date cannot be parsed
- GitHub Actions: HACS validation, hassfest, and unit tests
