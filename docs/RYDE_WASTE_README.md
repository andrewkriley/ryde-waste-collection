# Ryde Council Waste Collection Scraper

A Python script to programmatically fetch waste collection dates from the Ryde Council website.

## Features

- Fetches General Waste, Garden Organics, and Recycling collection dates
- Uses Selenium WebDriver for browser automation
- Handles Google Places autocomplete
- Supports any address in the Ryde LGA
- JSON output option for easy integration

## Requirements

- Python 3
- Google Chrome browser
- Internet connection

## Setup

The script uses a Python virtual environment with the following dependencies:
- selenium
- webdriver-manager
- beautifulsoup4

To set up (already done for you):

```bash
python3 -m venv /tmp/ryde_env
/tmp/ryde_env/bin/pip install selenium webdriver-manager beautifulsoup4
```

## Usage

### Basic Usage

```bash
/tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_waste_scraper.py "YOUR_ADDRESS"
```

### Get Help

```bash
/tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_waste_scraper.py --help
```

### JSON Output

```bash
/tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_waste_scraper.py "YOUR_ADDRESS" --json
```

Example JSON output:
```json
{
  "General Waste": "Wed 21/1/2026",
  "Garden Organics": "Wed 28/1/2026",
  "Recycling": "Wed 21/1/2026"
}
```

### Debug Mode

Save the page source for debugging:

```bash
/tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_waste_scraper.py "YOUR_ADDRESS" --debug
```

## How It Works

1. **Load Page**: Opens the Ryde Council "My area" page in a headless Chrome browser
2. **Find Input**: Locates the address input field (`txtAddressPublic-My-Area`)
3. **Enter Address**: Types the address and handles Google Places autocomplete
4. **Submit**: Clicks the search button (`btnSearch_Public-My-Area`)
5. **Extract Data**: Parses the resulting HTML for waste collection dates using regex patterns
6. **Output**: Displays the collection schedule

## Programmatic Integration

You can import and use the scraper in your own Python scripts:

```python
import sys
sys.path.insert(0, '/tmp/ryde_env/lib/python3.*/site-packages')

from ryde_waste_scraper import get_waste_collection_info

results = get_waste_collection_info("YOUR_ADDRESS")
if results:
    print(f"Next General Waste collection: {results['General Waste']}")
```

## Example Use Cases

### Shell Script Integration

```bash
#!/bin/bash
# Check if bins need to go out today

ADDRESS="YOUR_ADDRESS"
RESULT=$(/tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_waste_scraper.py "$ADDRESS" --json)

if [ $? -eq 0 ]; then
    echo "Waste Collection Schedule:"
    echo "$RESULT"
fi
```

### Cron Job

Add to crontab to get weekly reminders:

```bash
# Run every Sunday at 6 PM
0 18 * * 0 /tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_waste_scraper.py "YOUR_ADDRESS"
```

### Python Integration

```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def get_waste_dates(address):
    cmd = [
        '/tmp/ryde_env/bin/python',
        '/home/andreril/ryde-waste-collection/ryde_waste_scraper.py',
        address,
        '--json'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extract JSON from output (skip non-JSON lines)
        lines = result.stdout.strip().split('\n')
        for i, line in enumerate(lines):
            if line.startswith('{'):
                json_str = '\n'.join(lines[i:])
                return json.loads(json_str)
    return None

# Usage
dates = get_waste_dates("YOUR_ADDRESS")
if dates:
    for waste_type, date in dates.items():
        print(f"{waste_type}: {date}")
```

## Troubleshooting

### No results found

- Verify the address is in the Ryde LGA
- Check that you have internet connectivity
- Run with `--debug` flag to inspect the page source
- The page structure may have changed (check `/tmp/ryde_result.html`)

### Chrome driver issues

The script uses `webdriver-manager` which automatically downloads and manages ChromeDriver. If you encounter issues:

```bash
# Manually update webdriver-manager
/tmp/ryde_env/bin/pip install --upgrade webdriver-manager
```

### Slow execution

The script includes deliberate delays to allow JavaScript to load and the form to submit. Typical execution time is 15-25 seconds.

## Notes

- This script uses browser automation and is subject to changes in the website structure
- Respect the council's servers - don't run this too frequently
- The script runs in headless mode (no visible browser window)
- For production use, consider implementing caching to reduce server load

## License

This is a utility script for personal use. Respect the Ryde Council website's terms of service.
