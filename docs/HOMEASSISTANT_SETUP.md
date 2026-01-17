# Home Assistant Integration Setup Guide

## Overview

This integration fetches waste collection dates from Ryde Council and publishes them to Home Assistant sensors with a beautiful Mushroom card dashboard.

## Features

- ✅ Three sensors for waste collection types (General, Recycling, Garden)
- ✅ Color-coded indicators (Red, Yellow, Green)
- ✅ Indicators light up only when collection is within 7 days
- ✅ Automatic daily updates
- ✅ Optional notification reminders
- ✅ Beautiful Mushroom card dashboard

## Prerequisites

1. **Home Assistant** running and accessible
2. **Mushroom Cards** custom component installed in Home Assistant
3. **Long-Lived Access Token** from Home Assistant

## Step 1: Install Mushroom Cards (if not already installed)

### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Click on "Frontend"
3. Search for "Mushroom"
4. Install "Mushroom Cards"
5. Restart Home Assistant

### Manual Installation
1. Download from: https://github.com/piitaya/lovelace-mushroom
2. Copy to `/config/www/mushroom/`
3. Add to Lovelace resources

## Step 2: Create Home Assistant Long-Lived Access Token

1. In Home Assistant, click your profile (bottom left)
2. Scroll down to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Give it a name (e.g., "Ryde Waste Collection")
5. Copy the token (you'll only see it once!)

## Step 3: Test the Integration

Run the integration manually to test:

```bash
export HA_TOKEN="your_long_lived_access_token_here"
export HA_URL="http://homeassistant.local:8123"
export RYDE_ADDRESS="YOUR_ADDRESS"

./publish-to-homeassistant.sh
```

Or with direct arguments:

```bash
/tmp/ryde_env/bin/python ryde_to_homeassistant.py \
  "YOUR_ADDRESS" \
  --ha-url "http://192.168.1.100:8123" \
  --ha-token "your_token_here"
```

You should see output like:

```
Fetching waste collection dates for: YOUR_ADDRESS
============================================================
Loading page: https://www.ryde.nsw.gov.au/Information-Pages/My-area
...
✓ Published General Waste: Wed 21/1/2026 (in 4 days)
✓ Published Recycling: Wed 21/1/2026 (in 4 days)
✓ Published Garden Organics: Wed 28/1/2026 (in 11 days)

Published 3/3 sensors successfully
```

## Step 4: Verify Sensors in Home Assistant

1. Go to Developer Tools > States
2. Search for:
   - `sensor.waste_general`
   - `sensor.waste_recycling`
   - `sensor.waste_garden`
3. You should see the dates and attributes

## Step 5: Add the Dashboard Card

1. Edit your dashboard (or create a new one)
2. Add a new card
3. Choose "Manual" mode
4. Copy the contents of `homeassistant_mushroom_card.yaml`
5. Paste and save

Your dashboard should now show:
- **General Waste** with red indicator (when within 7 days)
- **Recycling** with yellow indicator (when within 7 days)
- **Garden Organics** with green indicator (when within 7 days)
- A summary chip showing the next upcoming collection

## Step 6: Set Up Automatic Updates

### Option A: Home Assistant Automation (Recommended)

1. Edit your Home Assistant `configuration.yaml`
2. Add the shell command:

```yaml
shell_command:
  update_ryde_waste: >
    /tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_to_homeassistant.py 
    "YOUR_ADDRESS" 
    --ha-url "http://homeassistant.local:8123" 
    --ha-token "YOUR_LONG_LIVED_ACCESS_TOKEN_HERE"
```

3. Add the automation (or use the UI to create it):

```yaml
automation:
  - id: update_ryde_waste_collection
    alias: Update Ryde Waste Collection
    trigger:
      - platform: time
        at: "06:00:00"
      - platform: homeassistant
        event: start
    action:
      - service: shell_command.update_ryde_waste
```

4. Reload automations or restart Home Assistant

### Option B: Cron Job

Add to your system crontab:

```bash
# Update waste collection data daily at 6 AM
0 6 * * * HA_TOKEN="your_token" HA_URL="http://homeassistant.local:8123" /home/andreril/ryde-waste-collection/publish-to-homeassistant.sh >> /var/log/ryde_waste.log 2>&1
```

## Step 7: Optional - Set Up Notifications

Add this automation to get reminded the evening before collection:

```yaml
automation:
  - id: waste_collection_reminder
    alias: Waste Collection Reminder
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: template
        value_template: >-
          {% set sensors = ['sensor.waste_general', 'sensor.waste_recycling', 'sensor.waste_garden'] %}
          {{ sensors | select('state_attr', 'days_until', 1) | list | length > 0 }}
    action:
      - service: notify.notify
        data:
          title: "Bins Tomorrow!"
          message: >-
            {% set bins = namespace(list=[]) %}
            {% if state_attr('sensor.waste_general', 'days_until') == 1 %}
              {% set bins.list = bins.list + ['General Waste'] %}
            {% endif %}
            {% if state_attr('sensor.waste_recycling', 'days_until') == 1 %}
              {% set bins.list = bins.list + ['Recycling'] %}
            {% endif %}
            {% if state_attr('sensor.waste_garden', 'days_until') == 1 %}
              {% set bins.list = bins.list + ['Garden Organics'] %}
            {% endif %}
            Remember to put out: {{ bins.list | join(', ') }}
```

## Sensor Attributes

Each sensor provides the following attributes:

- `friendly_name`: Display name
- `icon`: MDI icon
- `date`: ISO formatted date (YYYY-MM-DD)
- `days_until`: Number of days until collection
- `collection_type`: Type of waste
- `color`: Indicator color (red/yellow/green)
- `upcoming`: Boolean - true if within 7 days
- `last_updated`: When the data was last fetched

## Troubleshooting

### Sensors not appearing
- Check that the script ran successfully
- Verify your Home Assistant URL is correct
- Verify your access token is valid
- Check Home Assistant logs

### Indicators not lighting up
- Verify the collection is within 7 days
- Check the `upcoming` attribute in Developer Tools
- Refresh your browser cache

### Script fails
- Run with `--debug` flag to save page source
- Check internet connectivity
- Verify Chrome is installed

### Automation not running
- Check Home Assistant logs
- Verify shell_command syntax
- Test the shell command manually in Developer Tools

## Advanced Configuration

### Custom Update Frequency

Change the time in the automation:

```yaml
trigger:
  - platform: time
    at: "06:00:00"  # Change to your preferred time
```

### Different Address

Edit the shell_command or environment variable:

```bash
export RYDE_ADDRESS="YOUR_ADDRESS"
```

### Custom Notification Service

Replace `notify.notify` with your specific notification service:

```yaml
service: notify.mobile_app_your_phone
```

## Files Reference

- `ryde_to_homeassistant.py` - Main integration script
- `publish-to-homeassistant.sh` - Wrapper script
- `homeassistant_mushroom_card.yaml` - Dashboard card config
- `homeassistant_automation.yaml` - Automation examples

## Support

If you encounter issues:
1. Run the script with `--debug` flag
2. Check Home Assistant logs
3. Verify all prerequisites are met
4. Test the scraper independently first

---

**Last Updated**: 2026-01-17
