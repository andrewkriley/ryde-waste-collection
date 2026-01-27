# Customization Guide

## Dynamic Icon Colors

Make your waste collection icons change color automatically as collection day approaches!

### Overview

Icons will:
- **Stay grey/blue** (default) when collection is more than 7 days away
- **Turn to bin color** when collection is 7 days or fewer away (including today!)
- Match actual Ryde Council bin colors: 🔴 Red (General), 🟡 Yellow (Recycling), 🟢 Green (Garden)

This helps you quickly see which bins need attention soon!

---

## Full Dashboard Example

This complete dashboard configuration uses Mushroom cards with dynamic colors. You'll need to install **Mushroom** from HACS (Frontend → Mushroom).

### For a New Dashboard

Copy and paste this entire configuration when creating a new dashboard:

```yaml
title: Waste Collection
views:
  - title: Home
    path: home
    cards:
      - type: vertical-stack
        cards:
          - type: custom:mushroom-title-card
            title: Waste Collection
            subtitle: Next 7 Days
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_general_waste
            name: General Waste
            icon: mdi:trash-can
            icon_color: |-
              {% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') %}
              {% if days != none and days <= 7 %}
                red
              {% else %}
                grey
              {% endif %}
            primary_info: name
            secondary_info: state
            badge_icon: |-
              {% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') %}
              {% if days != none and days <= 1 %}
                mdi:alert
              {% endif %}
            badge_color: red
            tap_action:
              action: more-info
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_recycling
            name: Recycling
            icon: mdi:recycle
            icon_color: |-
              {% set days = state_attr('sensor.ryde_waste_collection_recycling', 'days_until') %}
              {% if days != none and days <= 7 %}
                yellow
              {% else %}
                grey
              {% endif %}
            primary_info: name
            secondary_info: state
            badge_icon: |-
              {% set days = state_attr('sensor.ryde_waste_collection_recycling', 'days_until') %}
              {% if days != none and days <= 1 %}
                mdi:alert
              {% endif %}
            badge_color: yellow
            tap_action:
              action: more-info
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_garden_organics
            name: Garden Organics
            icon: mdi:leaf
            icon_color: |-
              {% set days = state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') %}
              {% if days != none and days <= 7 %}
                green
              {% else %}
                grey
              {% endif %}
            primary_info: name
            secondary_info: state
            badge_icon: |-
              {% set days = state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') %}
              {% if days != none and days <= 1 %}
                mdi:alert
              {% endif %}
            badge_color: green
            tap_action:
              action: more-info
```

### For Adding to Existing Dashboard

If you want to add just the cards to an existing dashboard, copy only the inner `vertical-stack` section (starting from `- type: vertical-stack`).

---

## Troubleshooting Grey Icons

If all your icons are staying grey even when `days_until` is 0-7, try these steps:

### 1. Verify the Attribute Exists

1. Go to **Developer Tools** → **States**
2. Find `sensor.ryde_waste_collection_general_waste`
3. Check if `days_until` attribute exists and has a numeric value

### 2. Test the Template

Go to **Developer Tools** → **Template** and test:

```jinja2
{% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') %}
Days until: {{ days }}
Type: {{ days.__class__.__name__ }}
Is None: {{ days == none }}
Should color: {{ days != none and days <= 7 }}
```

Expected output when `days_until = 0`:
```
Days until: 0
Type: int
Is None: False
Should color: True
```

### 3. Alternative Template Syntax

If the standard template isn't working, try this alternative:

```yaml
icon_color: |-
  {% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') != none and state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 7 %}
    red
  {% else %}
    grey
  {% endif %}
```

Or use numeric comparison without variable:

```yaml
icon_color: >-
  {{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') or 999) <= 7 else 'grey' }}
```

### 4. Check Mushroom Version

Make sure you have the latest version of Mushroom cards:
1. Go to **HACS** → **Frontend**
2. Find **Mushroom**
3. Update if available
4. Restart Home Assistant

### 5. Clear Browser Cache

Sometimes cached card configurations cause issues:
1. Clear your browser cache
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Reopen the dashboard

---

## Customizing the Threshold

Want to change when icons become colored? Adjust the number in the comparison:

**3 days notice** (collection very soon):
```yaml
{% if days != none and days <= 3 %}
```

**14 days notice** (two weeks ahead):
```yaml
{% if days != none and days <= 14 %}
```

---

## Color Reference

Matching actual Ryde Council bin colors:

| Waste Type | When Colored | Icon Color | Otherwise |
|------------|--------------|------------|-----------|
| General Waste | 0-7 days | `red` | `grey` |
| Recycling | 0-7 days | `yellow` | `grey` |
| Garden Organics | 0-7 days | `green` | `grey` |

**Note**: `days_until = 0` means collection is **today** - it will show colored!

---

## Installing Mushroom Cards

1. Open **HACS** in Home Assistant
2. Go to **Frontend**
3. Click **Explore & Download Repositories**
4. Search for **Mushroom**
5. Click **Download**
6. Restart Home Assistant
7. Use the dashboard configuration above

---

## Why Dynamic Colors?

- **At a glance**: Quickly see which bins are due soon
- **Less clutter**: Icons only stand out when relevant
- **Smart reminders**: Visual cue without notifications
- **Customizable**: Adjust the threshold to your preference

The icons will automatically update as collection day approaches!
