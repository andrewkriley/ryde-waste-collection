# Ryde Council waste collection APIs

This integration uses two public City of Ryde endpoints. It is unofficial and will break if the council changes those APIs or the HTML they return.

Implementation lives in `custom_components/ryde_waste_collection/api.py`.

## Endpoints

### Address search

`GET https://www.ryde.nsw.gov.au/api/v1/myarea/search?keywords=128+Blaxland+Road+Ryde+2112`

Returns ranked matches. The first result is not always the street address the user typed (for example a unit in a large complex may rank first). Setup therefore shows a picker when more than one match is returned, and stores the chosen `Id` as `geolocation_id`.

### Waste services

`GET https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices?geolocationid=<id>&ocsvclang=en-AU`

JSON body:

```json
{
  "success": true,
  "responseContent": "<div>...HTML with next-service dates...</div>"
}
```

Dates are extracted from:

```html
<h3>General Waste</h3>
<div class="next-service">Tue 25/8/2026</div>
```

The same markup is used for Garden Organics and Recycling.

## Request headers

The council front-end is behind Akamai. Requests send:

- `User-Agent: HomeAssistant/ryde_waste_collection`
- `Accept: application/json`
- `Referer: https://www.ryde.nsw.gov.au/`

Chrome-like user agents have been observed returning HTTP 403.

## Parsing rules

- Input date text looks like `Tue 25/8/2026`
- `days_until` is calculated in the Home Assistant timezone
- If the date cannot be parsed, `days_until` is omitted (`None`) instead of `0`

## Tests

Parser fixtures are in `tests/fixtures/`. Run:

```bash
pytest -q
```
