# Brand icons

Home Assistant 2026.3+ loads custom-integration icons from a `brand/` directory inside the integration. That is the official path. Do not open a pull request against [home-assistant/brands](https://github.com/home-assistant/brands) for this repository: new `custom_integrations/*` PRs are auto-closed.

## Files that matter

HACS validation and Home Assistant both read:

```
custom_components/ryde_waste_collection/brand/icon.png
custom_components/ryde_waste_collection/brand/icon@2x.png
custom_components/ryde_waste_collection/brand/dark_icon.png
custom_components/ryde_waste_collection/brand/dark_icon@2x.png
```

| File | Size |
| --- | --- |
| `icon.png` / `dark_icon.png` | 256×256 PNG |
| `icon@2x.png` / `dark_icon@2x.png` | 512×512 PNG |

The same files are copied under `brand/` and `brands_submission/ryde_waste_collection/` for convenience. Keep `custom_components/ryde_waste_collection/brand/` as the source of truth.

## Where the icon appears

- **Settings → Devices & services** (Add Integration picker and the integration device page) on Home Assistant 2026.3+
- Local API: `/api/brands/integration/ryde_waste_collection/icon.png`

The HACS downloads panel still requests the public brands CDN in current HACS releases, so it can show “icon not available” even when the local files are present. See [hacs/integration#5223](https://github.com/hacs/integration/issues/5223).
