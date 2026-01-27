# Customization Guide

## Dynamic Icon Colors

Make your waste collection icons change color automatically as collection day approaches!

### Overview

Icons will:
- **Stay grey/blue** (default) when collection is more than 7 days away
- **Turn to bin color** when collection is 7 days or fewer away (including today!)
- Match actual Ryde Council bin colors: 🔴 Red (General), 🟡 Yellow (Recycling), 🟢 Green (Garden)

---

## Full Dashboard Example

This complete dashboard configuration uses Mushroom cards with dynamic colors. Install **Mushroom** from HACS (Frontend → Mushroom) first.

### Complete Dashboard YAML

**Copy this entire configuration:**

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
            icon_color: "{{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}"
            primary_info: name
            secondary_info: state
            badge_icon: "{{ 'mdi:alert' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 2) else '' }}"
            badge_color: red
            tap_action:
              action: more-info
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_recycling
            name: Recycling
            icon: mdi:recycle
            icon_color: "{{ 'yellow' if (state_attr('sensor.ryde_waste_collection_recycling', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}"
            primary_info: name
            secondary_info: state
            badge_icon: "{{ 'mdi:alert' if (state_attr('sensor.ryde_waste_collection_recycling', 'days_until') | int(-1)) in range(0, 2) else '' }}"
            badge_color: yellow
            tap_action:
              action: more-info
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_garden_organics
            name: Garden Organics
            icon: mdi:leaf
            icon_color: "{{ 'green' if (state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}"
            primary_info: name
            secondary_info: state
            badge_icon: "{{ 'mdi:alert' if (state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') | int(-1)) in range(0, 2) else '' }}"
            badge_color: green
            tap_action:
              action: more-info
```

### Key Points

**The critical syntax for icon_color:**
```yaml
icon_color: "{{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}"
```

**Why this works:**
- Single-line template (no extra whitespace)
- Uses `in range(0, 8)` which means 0-7 (range is exclusive at the end)
- `| int(-1)` converts to integer with -1 default (which is not in range 0-8)
- Quoted string for proper YAML parsing

---

## Troubleshooting

### If Icons Are Still Grey

**1. Test the template in Developer Tools → Template:**

```jinja2
{% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
Days: {{ days }}
In range: {{ days in range(0, 8) }}
Color: {{ 'red' if days in range(0, 8) else 'grey' }}
```

**2. Check the exact output:**
- Should show `Color: red` when days is 0-7
- Should show `Color: grey` when days is 8+ or -1

**3. Verify sensor state:**
- Go to Developer Tools → States
- Find `sensor.ryde_waste_collection_general_waste`
- Confirm `days_until` attribute exists and is a number

**4. Try the alternative syntax with >-:**

```yaml
icon_color: >-
  {{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}
```

**5. Make sure you're editing the right dashboard:**
- Save your changes
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check you're viewing the correct dashboard tab

### Common Mistakes

❌ **Wrong - Has whitespace issues:**
```yaml
icon_color: |-
  {% set days = ... %}
  {% if days >= 0 %}
    red
  {% endif %}
```

✅ **Correct - Single line, no whitespace:**
```yaml
icon_color: "{{ 'red' if (state_attr('sensor...', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}"
```

---

## Customizing the Threshold

Change the range to adjust when colors appear:

**3 days notice:**
```yaml
icon_color: "{{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 4) else 'grey' }}"
```

**14 days notice:**
```yaml
icon_color: "{{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 15) else 'grey' }}"
```

Remember: `range(0, 8)` = 0 through 7 (range end is exclusive)

---

## Understanding range()

- `range(0, 8)` includes: 0, 1, 2, 3, 4, 5, 6, 7
- `range(0, 4)` includes: 0, 1, 2, 3
- `range(0, 15)` includes: 0, 1, 2, 3, ..., 14

The second number is **exclusive** (not included).

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

## Color Reference

| Waste Type | When Colored | Icon Color | Otherwise |
|------------|--------------|------------|-----------|
| General Waste | 0-7 days | `red` | `grey` |
| Recycling | 0-7 days | `yellow` | `grey` |
| Garden Organics | 0-7 days | `green` | `grey` |

**Alert badges** appear when collection is today (0) or tomorrow (1).

---

## Still Not Working?

If you've tried everything above and it still doesn't work:

1. **Copy the EXACT YAML** from the "Complete Dashboard YAML" section above
2. **Create a NEW dashboard** (don't edit existing) to test
3. **Clear browser cache** completely
4. **Restart Home Assistant**
5. **Check Mushroom version** - update if old

The single-line template format is critical for Mushroom cards to parse the color correctly.
