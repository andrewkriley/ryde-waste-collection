# Project Structure

All Ryde Waste Collection files are now organized in:
**`/home/andreril/ryde-waste-collection/`**

## Directory Contents

```
ryde-waste-collection/
├── Core Scripts
│   ├── ryde_waste_scraper.py       - Main scraper using Selenium
│   ├── ryde_to_homeassistant.py    - Home Assistant integration
│   ├── get-ryde-bins.sh            - Standalone wrapper script
│   └── publish-to-homeassistant.sh - HA integration wrapper
│
├── Configuration Files
│   ├── homeassistant_mushroom_card.yaml    - Dashboard card
│   └── homeassistant_automation.yaml       - Automation examples
│
└── Documentation
    ├── README.md                      - Main overview
    ├── PROJECT_STRUCTURE.md           - This file
    ├── QUICK_START.md                 - Standalone quick start
    ├── HOMEASSISTANT_QUICKSTART.md    - HA quick start
    ├── HOMEASSISTANT_SETUP.md         - Full HA setup guide
    ├── VISUAL_EXAMPLE.md              - Dashboard visuals
    └── RYDE_WASTE_README.md           - Original scraper docs
```

## Usage from Anywhere

### Option 1: Run from project directory
```bash
cd /home/andreril/ryde-waste-collection
./get-ryde-bins.sh "YOUR_ADDRESS"
```

### Option 2: Run with full path
```bash
/home/andreril/ryde-waste-collection/get-ryde-bins.sh "YOUR_ADDRESS"
```

### Option 3: Add to PATH (optional)
```bash
echo 'export PATH="$PATH:/home/andreril/ryde-waste-collection"' >> ~/.bashrc
source ~/.bashrc

# Now you can run from anywhere:
get-ryde-bins.sh "YOUR_ADDRESS"
```

## Home Assistant Configuration

Update your Home Assistant `configuration.yaml` with the new path:

```yaml
shell_command:
  update_ryde_waste: >
    /tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_to_homeassistant.py 
    "YOUR_ADDRESS" 
    --ha-url "http://homeassistant.local:8123" 
    --ha-token "YOUR_TOKEN"
```

## Virtual Environment

The Python virtual environment remains at:
**`/tmp/ryde_env/`**

This is shared across all scripts and contains:
- selenium
- webdriver-manager
- beautifulsoup4
- requests

## Quick Commands

```bash
# Change to project directory
cd ~/ryde-waste-collection

# Run standalone scraper
./get-ryde-bins.sh "YOUR_ADDRESS"

# Publish to Home Assistant
export HA_TOKEN="your_token"
./publish-to-homeassistant.sh

# Get help
./get-ryde-bins.sh --help
```

## File Permissions

All shell scripts (`.sh`) are executable:
- `get-ryde-bins.sh`
- `publish-to-homeassistant.sh`

All Python scripts (`.py`) are executable:
- `ryde_waste_scraper.py`
- `ryde_to_homeassistant.py`

---

All paths in documentation and scripts have been updated to reflect this new structure.
