# Quick Start Guide

## What You Have

A working scraper that fetches waste collection dates from the Ryde Council website for any address.

## Files Created

1. **`ryde_waste_scraper.py`** - Main Python scraper script
2. **`get-ryde-bins.sh`** - Convenient bash wrapper
3. **`RYDE_WASTE_README.md`** - Full documentation
4. **`QUICK_START.md`** - This file

## Quickest Way to Use

### Simple Command
```bash
./get-ryde-bins.sh "YOUR_ADDRESS"
```

### Get JSON Output
```bash
./get-ryde-bins.sh "YOUR_ADDRESS" --json
```

### Try Another Address
```bash
./get-ryde-bins.sh "YOUR_ADDRESS"
```

## What It Returns

For "YOUR_ADDRESS", you'll get:

```
WASTE COLLECTION SCHEDULE
============================================================
General Waste: Wed 21/1/2026
Garden Organics: Wed 28/1/2026
Recycling: Wed 21/1/2026
============================================================
```

## How It Works

1. Opens the Ryde Council website in a headless Chrome browser
2. Finds the address search field
3. Enters your address
4. Clicks search
5. Extracts the waste collection dates from the results
6. Displays them in a clean format

## Technical Details

- **Language**: Python 3
- **Dependencies**: Selenium, WebDriver Manager, BeautifulSoup4
- **Virtual Environment**: `/tmp/ryde_env`
- **Execution Time**: ~15-25 seconds
- **Mode**: Headless (no visible browser window)

## Integration Examples

### Use in Shell Script
```bash
#!/bin/bash
DATES=$(./get-ryde-bins.sh "YOUR_ADDRESS" --json)
echo "$DATES"
```

### Use in Cron Job
```bash
# Check bins every Sunday at 6 PM
0 18 * * 0 /home/andreril/ryde-waste-collection/get-ryde-bins.sh "YOUR_ADDRESS"
```

### Use in Python
```python
import subprocess
result = subprocess.run(
    ['./get-ryde-bins.sh', 'YOUR_ADDRESS', '--json'],
    capture_output=True,
    text=True
)
print(result.stdout)
```

## Troubleshooting

If it doesn't work:

1. Make sure you have internet connection
2. Make sure Chrome is installed: `which google-chrome`
3. Check the virtual environment exists: `ls /tmp/ryde_env`
4. Run with debug flag: `./get-ryde-bins.sh "YOUR_ADDRESS" --debug`

## Next Steps

- Read `RYDE_WASTE_README.md` for full documentation
- Try different addresses in the Ryde area
- Integrate into your own scripts or automation

---

**Created**: 2026-01-17  
**Tested With**: YOUR_ADDRESS  
**Last Successful Run**: Wed 21/1/2026, Wed 28/1/2026
