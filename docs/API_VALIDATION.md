# Ryde Council Waste Collection - API Documentation

## Overview
This project uses Ryde Council's public APIs to retrieve waste collection schedules. This approach replaced the previous Selenium-based screen scraping method for improved reliability and performance.

## API Endpoints

### 1. Address Search API
**Endpoint:** `https://www.ryde.nsw.gov.au/api/v1/myarea/search`

**Method:** GET

**Parameters:**
- `keywords` (string): The address to search for

**Example Request:**
```
https://www.ryde.nsw.gov.au/api/v1/myarea/search?keywords=129+Blaxland+Road%2C+Ryde
```

**Response Format:**
```json
{
  "Items": [
    {
      "Id": "b148f7d7-e435-4b28-8970-b89af8be2ba0",
      "AddressSingleLine": "1028/109-129 Blaxland Road, Ryde 2112",
      "MunicipalSubdivision": null,
      "Distance": 0,
      "Score": 15.635677,
      "LatLon": null
    }
  ],
  "Offset": 0,
  "Limit": 10,
  "Total": 1
}
```

**Notes:**
- Returns multiple potential matches ranked by Score
- First result (highest score) is typically the correct match
- `Id` field is required for the waste services API

### 2. Waste Services API
**Endpoint:** `https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices`

**Method:** GET

**Parameters:**
- `geolocationid` (string): The ID from the address search API
- `ocsvclang` (string): Language parameter (use "en-AU")

**Example Request:**
```
https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices?geolocationid=b148f7d7-e435-4b28-8970-b89af8be2ba0&ocsvclang=en-AU
```

**Response Format:**
```json
{
  "success": true,
  "responseContent": "<div>...HTML content with waste collection dates...</div>"
}
```

**Notes:**
- Response contains HTML that needs to be parsed
- HTML includes dates for General Waste, Garden Organics, and Recycling
- Date format: "Day DD/M/YYYY" (e.g., "Tue 27/1/2026")

## Advantages Over Screen Scraping

1. **More Reliable:** API endpoints are less likely to break with website redesigns
2. **Cleaner Data:** JSON response format is easier to parse than HTML
3. **Better Performance:** Direct API calls are faster than browser automation
4. **No Browser Dependencies:** Eliminates need for Selenium and Chrome/Chromium
5. **Official Support:** Using public APIs that Ryde Council's website uses internally
6. **Structured Data:** Address search returns normalized address data with geolocation IDs

## Implementation

### Python Example
The `ryde_waste_scraper.py` script provides a complete implementation:

```python
from ryde_waste_scraper import get_waste_collection_info

waste_info = get_waste_collection_info("129 Blaxland Road, Ryde")
print(waste_info)
# Output: {'General Waste': 'Tue 27/1/2026', 'Garden Organics': 'Tue 27/1/2026', 'Recycling': 'Tue 3/2/2026'}
```

### Dependencies
- `requests` library for HTTP requests
- Standard library modules: `json`, `re`, `html`, `sys`, `argparse`

### Parsing Logic
The waste services API returns HTML content that must be parsed:
```python
import re
from html import unescape

html_content = unescape(response_content)
general_waste = re.search(
    r'<h3>General Waste</h3>.*?<div class="next-service">\s*(.+?)\s*</div>',
    html_content,
    re.DOTALL
).group(1).strip()
```

## Command-Line Usage

### Basic Usage
```bash
python3 ryde_waste_scraper.py "129 Blaxland Road, Ryde"
```

### JSON Output
```bash
python3 ryde_waste_scraper.py "129 Blaxland Road, Ryde" --json
```

## API Validation

To validate the API implementation, run:

```bash
python3 api_validation.py
```

This tests the address search and waste schedule retrieval to ensure the APIs are working correctly.

## Integration with Home Assistant


## Error Handling

The implementation includes robust error handling for:
- Network timeouts and connection errors
- Invalid addresses (no search results)
- API response parsing errors
- Missing or malformed data

All errors are logged to stderr for easy debugging.

## Migration Notes

The API-based approach maintains the same `get_waste_collection_info(address)` function interface as the previous Selenium-based scraper.
