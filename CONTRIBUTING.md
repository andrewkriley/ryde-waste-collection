# Contributing to Ryde Waste Collection

## Reporting bugs

Open an issue with:

- What happened and what you expected
- Steps to reproduce
- Home Assistant version and how you installed the integration
- Logs with addresses or other personal data removed

## Pull requests

1. Fork the repository and create a feature branch
2. Keep changes focused
3. Update documentation when behaviour changes
4. Run the unit tests:

```bash
pip install pytest aiohttp
pytest -q
```

5. Use conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`)

## Code style

- Follow PEP 8
- Keep HTTP and HTML parsing in `api.py` so it can be tested without Home Assistant
- Use Home Assistant's shared aiohttp session (`async_get_clientsession`)
- Do not treat a parse failure as collection today (`days_until` must be `None`)

## Local Home Assistant install

Use Home Assistant 2026.3 or later (2026.10 is the current target). Link the integration directory, not the repository root:

```bash
ln -s /path/to/ryde-waste-collection/custom_components/ryde_waste_collection \
  /path/to/homeassistant/custom_components/ryde_waste_collection
```

Restart Home Assistant and add the integration from the UI. The bins logo comes from `custom_components/ryde_waste_collection/brand/`.

## Code of conduct

Be respectful and constructive.


### Running regression tests

The API tests do not require Home Assistant:

```sh
python -m pip install pytest aiohttp
python -m pytest -q --ignore=tests/ha
```

Run the lifecycle tests in a separate Python 3.14 environment:

```sh
python -m pip install -r requirements-test-ha.txt
python -m pytest tests/ha -q --asyncio-mode=auto
```

The pinned test helper includes Home Assistant 2026.10.4. These tests load real
config entries, sensors, coordinators and timers, replacing only council network
calls. They verify Sydney midnight day-count updates, successful unload cleanup
(including the options listener), retained operation when platform unload fails,
and setup after unload without duplicate midnight refreshes. Frozen time avoids
waiting for real midnight. Both suites run in CI.


## Release process

Merging to main does not publish a GitHub/HACS release. The repository currently
uses manually created GitHub releases; no release automation is configured.

1. Choose a patch increment for compatible bug fixes, a minor increment for new
   public features, and a major increment for breaking changes. The reliability
   fixes in PR #7 are version 1.1.2, following 1.1.1.
2. Include the version change in the implementation PR before merging. Keep
   manifest.json, the API User-Agent, README version and API header documentation
   aligned, and add release notes to CHANGELOG.md.
3. Run both test suites and all CI checks. Smoke-test live address search and
   waste schedules with the new User-Agent, since the council WAF filters it.
4. Merge only after checks pass. Confirm the main workflow also passes.
5. When publication is approved, create a tag matching the manifest version
   (for example, 1.1.2, following the existing tags without a v prefix) at the
   validated main commit, then publish a GitHub release using the changelog
   notes. Verify the release tag and downloadable integration version match.
6. Confirm HACS offers the published version; merging alone is not evidence of
   release availability.
