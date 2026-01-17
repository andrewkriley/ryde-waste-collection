# Home Assistant Dashboard Setup Guide

Complete guide to setting up your waste collection dashboard with Mushroom cards.

## Overview

With MQTT Discovery, the sensors are **created automatically** when the container runs. You only need to:
1. Install Mushroom Cards (UI component)
2. Add the dashboard card configuration

## Prerequisites

- ✅ MQTT broker configured and running
- ✅ Container running and publishing to MQTT
- ✅ Sensors auto-discovered in Home Assistant

## Step 1: Verify Sensors Exist

Before creating the dashboard, verify the sensors were auto-created:

### Method A: Via Devices & Services

1. Go to **Settings** → **Devices & Services**
2. Click **MQTT**
3. Look for device: **"Ryde Waste Collection"**
4. Click on it - you should see 3 sensors:
   - General Waste Collection
   - Recycling Collection
   - Garden Organics Collection

### Method B: Via Developer Tools

1. Go to **Developer Tools** → **States**
2. Search for: `ryde_waste`
3. You should see:
   - `sensor.ryde_waste_general`
   - `sensor.ryde_waste_recycling`
   - `sensor.ryde_waste_garden`

**If sensors don't exist yet:**
- Wait 1-2 minutes for container to run first update
- Check container logs: `docker-compose logs -f`
- See troubleshooting section below

## Step 2: Install Mushroom Cards

Mushroom Cards provide the beautiful UI components for the dashboard.

### Via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Click **Frontend**
3. Click **+ Explore & Download Repositories**
4. Search for **"Mushroom"**
5. Click **"Mushroom Cards"** by piitaya
6. Click **Download**
7. Click **Download** again to confirm
8. **Restart Home Assistant**:
   - Settings → System → Restart

### Manual Installation (Alternative)

1. Download latest release from: https://github.com/piitaya/lovelace-mushroom/releases
2. Extract files
3. Copy `mushroom.js` to `/config/www/mushroom/`
4. Add to Lovelace resources:
   - Settings → Dashboards → Resources tab
   - Add resource: `/local/mushroom/mushroom.js`
   - Type: JavaScript Module
5. Restart Home Assistant

### Verify Installation

1. Go to any dashboard
2. Click **Edit Dashboard**
3. Click **+ Add Card**
4. Search for "mushroom"
5. You should see various Mushroom card types

## Step 3: Create the Dashboard

### Option A: Create New Dashboard (Recommended for First Time)

1. Go to **Settings** → **Dashboards**
2. Click **+ Add Dashboard**
3. Fill in:
   - **Name**: Waste Collection
   - **Icon**: mdi:trash-can
   - **Show in sidebar**: ✓
4. Click **Create**
5. Click **Take Control** (if using UI mode)

### Option B: Use Existing Dashboard

Skip to Step 4 if adding to an existing dashboard.

## Step 4: Add the Waste Collection Card

### Get the Card Configuration

The complete card configuration is in: `homeassistant_mushroom_card.yaml`

You can view it with:
```bash
cat homeassistant_mushroom_card.yaml
```

### Add to Dashboard

1. Open your dashboard
2. Click **✏️ Edit** (top right)
3. Click **+ Add Card** (bottom right)
4. Scroll down and click **Manual**
5. **Copy the entire contents** of `homeassistant_mushroom_card.yaml`
6. **Paste** into the card editor
7. Click **Save**
8. Click **Done** to exit edit mode

## What You'll See

Your dashboard will display:

### Title Section
```
🗑️ Waste Collection
   Ryde Council - Next Collections
```

### Three Collection Cards

**General Waste** 🔴
- Icon: Trash can
- Shows: "Wed 21/1/2026 (4 days)"
- Red indicator when within 7 days
- Bell badge when upcoming

**Recycling** 🟡
- Icon: Recycle symbol
- Shows: "Wed 21/1/2026 (4 days)"
- Yellow indicator when within 7 days
- Bell badge when upcoming

**Garden Organics** 🟢
- Icon: Leaf
- Shows: "Wed 28/1/2026 (11 days)"
- Green indicator when within 7 days
- Bell badge when upcoming

### Summary Chip
```
📅 Next: General Waste in 4 days
```

## Step 5: Customize (Optional)

### Change Colors

Edit the card YAML and modify `icon_color`:

```yaml
icon_color: >-
  {% if state_attr('sensor.ryde_waste_general', 'upcoming') == true %}
    red  # Change to: blue, orange, purple, etc.
  {% else %}
    grey
  {% endif %}
```

### Change Icons

Modify the `icon` field:
```yaml
icon: mdi:trash-can  # Change to any MDI icon
```

Browse icons at: https://pictogrammers.com/library/mdi/

### Reorder Cards

In edit mode, drag and drop cards to reorder them.

### Add More Cards

Add additional Mushroom cards like:
- **Mushroom Entity Card** - For detailed sensor info
- **Mushroom Chips Card** - For quick status
- **Mushroom Title Card** - For section headers

## Complete Card Configuration

Here's the full card configuration (also in `homeassistant_mushroom_card.yaml`):

```yaml
type: vertical-stack
cards:
  # Title Card
  - type: custom:mushroom-title-card
    title: Waste Collection
    subtitle: Ryde Council - Next Collections

  # General Waste Card
  - type: custom:mushroom-template-card
    primary: General Waste
    secondary: >-
      {% if states('sensor.ryde_waste_general') != 'unknown' %}
        {{ states('sensor.ryde_waste_general') }}
        {% if state_attr('sensor.ryde_waste_general', 'days_until') is not none %}
          ({{ state_attr('sensor.ryde_waste_general', 'days_until') }} days)
        {% endif %}
      {% else %}
        No data available
      {% endif %}
    icon: mdi:trash-can
    icon_color: >-
      {% if state_attr('sensor.ryde_waste_general', 'upcoming') == true %}
        red
      {% else %}
        grey
      {% endif %}
    badge_icon: >-
      {% if state_attr('sensor.ryde_waste_general', 'upcoming') == true %}
        mdi:bell-ring
      {% endif %}
    badge_color: red
    tap_action:
      action: more-info
    entity: sensor.ryde_waste_general

  # Recycling Card (similar structure)
  - type: custom:mushroom-template-card
    primary: Recycling
    secondary: >-
      {% if states('sensor.ryde_waste_recycling') != 'unknown' %}
        {{ states('sensor.ryde_waste_recycling') }}
        {% if state_attr('sensor.ryde_waste_recycling', 'days_until') is not none %}
          ({{ state_attr('sensor.ryde_waste_recycling', 'days_until') }} days)
        {% endif %}
      {% else %}
        No data available
      {% endif %}
    icon: mdi:recycle
    icon_color: >-
      {% if state_attr('sensor.ryde_waste_recycling', 'upcoming') == true %}
        yellow
      {% else %}
        grey
      {% endif %}
    badge_icon: >-
      {% if state_attr('sensor.ryde_waste_recycling', 'upcoming') == true %}
        mdi:bell-ring
      {% endif %}
    badge_color: yellow
    tap_action:
      action: more-info
    entity: sensor.ryde_waste_recycling

  # Garden Organics Card (similar structure)
  - type: custom:mushroom-template-card
    primary: Garden Organics
    secondary: >-
      {% if states('sensor.ryde_waste_garden') != 'unknown' %}
        {{ states('sensor.ryde_waste_garden') }}
        {% if state_attr('sensor.ryde_waste_garden', 'days_until') is not none %}
          ({{ state_attr('sensor.ryde_waste_garden', 'days_until') }} days)
        {% endif %}
      {% else %}
        No data available
      {% endif %}
    icon: mdi:leaf
    icon_color: >-
      {% if state_attr('sensor.ryde_waste_garden', 'upcoming') == true %}
        green
      {% else %}
        grey
      {% endif %}
    badge_icon: >-
      {% if state_attr('sensor.ryde_waste_garden', 'upcoming') == true %}
        mdi:bell-ring
      {% endif %}
    badge_color: green
    tap_action:
      action: more-info
    entity: sensor.ryde_waste_garden

  # Next Collection Summary
  - type: custom:mushroom-chips-card
    chips:
      - type: template
        icon: mdi:calendar-check
        content: >-
          {% set upcoming = namespace(found=false, min_days=999, type='') %}
          {% for sensor in ['sensor.ryde_waste_general', 'sensor.ryde_waste_recycling', 'sensor.ryde_waste_garden'] %}
            {% if state_attr(sensor, 'days_until') is not none and state_attr(sensor, 'days_until') >= 0 %}
              {% if state_attr(sensor, 'days_until') < upcoming.min_days %}
                {% set upcoming.min_days = state_attr(sensor, 'days_until') %}
                {% set upcoming.type = state_attr(sensor, 'collection_type') %}
                {% set upcoming.found = true %}
              {% endif %}
            {% endif %}
          {% endfor %}
          {% if upcoming.found %}
            Next: {{ upcoming.type }} in {{ upcoming.min_days }} day{{ 's' if upcoming.min_days != 1 else '' }}
          {% else %}
            No upcoming collections
          {% endif %}
        icon_color: blue
```

## Troubleshooting

### Card Shows "Custom element doesn't exist: custom:mushroom-title-card"

**Cause:** Mushroom Cards not installed properly

**Solution:**
1. Install Mushroom Cards via HACS (see Step 2)
2. Restart Home Assistant
3. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)

### Card Shows "Entity not available: sensor.ryde_waste_general"

**Cause:** Sensors not created yet

**Solution:**
1. Check container is running: `docker-compose ps`
2. Check container logs: `docker-compose logs -f`
3. Verify MQTT connection in logs: "✓ Connected to MQTT broker"
4. Wait 1-2 minutes for first update
5. Check Developer Tools → States for sensors

### Card Shows "No data available"

**Cause:** Sensors exist but have no data yet

**Solution:**
1. Wait for container to complete first scrape
2. Check logs show: "✓ Published General Waste: ..."
3. May take 15-30 seconds for scrape to complete
4. Refresh dashboard

### Colors Not Showing

**Cause:** Indicators only show when within 7 days

**Solution:**
- This is normal behavior
- Grey icon means collection is more than 7 days away
- Icon lights up (red/yellow/green) when within 7 days
- To test, you can temporarily modify the template to always show color

### Card Layout Issues

**Solution:**
- Use vertical-stack type (as shown in example)
- Each card should be properly indented
- Ensure YAML syntax is correct
- Use YAML validator if needed

## Mobile View

The dashboard works perfectly on mobile:
- Cards stack vertically
- Touch-friendly
- Same functionality as desktop
- Looks great on Home Assistant app

## Adding to Home Screen

### iOS
1. Open dashboard in Safari
2. Tap Share button
3. Tap "Add to Home Screen"

### Android
1. Open dashboard in Chrome
2. Tap menu (three dots)
3. Tap "Add to Home screen"

## Advanced: Notifications

Add automations to get notified about upcoming collections:

```yaml
# automation.yaml or via UI
automation:
  - alias: Bin Reminder Evening Before
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: template
        value_template: >-
          {% set sensors = ['sensor.ryde_waste_general', 'sensor.ryde_waste_recycling', 'sensor.ryde_waste_garden'] %}
          {{ sensors | select('state_attr', 'days_until', 1) | list | length > 0 }}
    action:
      - service: notify.notify
        data:
          title: "Bins Tomorrow!"
          message: >-
            {% set bins = [] %}
            {% if state_attr('sensor.ryde_waste_general', 'days_until') == 1 %}
              {% set bins = bins + ['General Waste'] %}
            {% endif %}
            {% if state_attr('sensor.ryde_waste_recycling', 'days_until') == 1 %}
              {% set bins = bins + ['Recycling'] %}
            {% endif %}
            {% if state_attr('sensor.ryde_waste_garden', 'days_until') == 1 %}
              {% set bins = bins + ['Garden Organics'] %}
            {% endif %}
            Remember to put out: {{ bins | join(', ') }}
```

## Summary

**What happens automatically:**
- ✅ Sensors created via MQTT Discovery
- ✅ Data published by container
- ✅ Attributes updated automatically

**What you need to do:**
1. ✅ Install Mushroom Cards
2. ✅ Copy card YAML to dashboard
3. ✅ Done!

**No manual sensor configuration needed!** Everything is automatic via MQTT Discovery.

---

**Need help?** See:
- [HOMEASSISTANT_MQTT_SETUP.md](HOMEASSISTANT_MQTT_SETUP.md) - MQTT setup
- [MQTT.md](../MQTT.md) - MQTT integration details
- [DOCKER.md](../DOCKER.md) - Container configuration
