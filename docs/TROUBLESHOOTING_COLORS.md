# Troubleshooting Icon Colors

Your template test returns `Days: 0, Should color: True`, which means the logic is correct but Mushroom isn't applying the color. Let's systematically test.

## Step 1: Test Static Color (No Template)

Add this card to your dashboard to verify Mushroom can show colors at all:

```yaml
- type: custom:mushroom-entity-card
  entity: sensor.ryde_waste_collection_general_waste
  name: TEST - Static Red
  icon: mdi:trash-can
  icon_color: red
```

**Expected**: Icon should be red.
**If not red**: Mushroom is not installed or configured correctly.

---

## Step 2: Test Simple Template

If static works, try the simplest template:

```yaml
- type: custom:mushroom-entity-card
  entity: sensor.ryde_waste_collection_general_waste
  name: TEST - Template Red
  icon: mdi:trash-can
  icon_color: "{{ 'red' }}"
```

**Expected**: Icon should be red.
**If not red**: Your Mushroom version doesn't support templates in `icon_color`.

---

## Step 3: Check Mushroom Version

Mushroom card templates for `icon_color` were added in a specific version.

1. Go to **HACS** → **Frontend**
2. Find **Mushroom**
3. Check version - you need **v2.0.0 or higher**
4. If older, click **Update**
5. Restart Home Assistant

---

## Step 4: Alternative - Use card-mod Instead

If Mushroom templates don't work, use `card-mod` which definitely supports this:

### Install card-mod
1. **HACS** → **Frontend** → Search "card-mod"
2. Install and restart

### Use This Configuration

```yaml
- type: custom:mushroom-entity-card
  entity: sensor.ryde_waste_collection_general_waste
  name: General Waste
  icon: mdi:trash-can
  primary_info: name
  secondary_info: state
  card_mod:
    style: |
      mushroom-shape-icon {
        {% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
        --icon-color: {% if days in range(0, 8) %}rgb(244, 67, 54){% else %}rgb(128, 128, 128){% endif %} !important;
        --shape-color: {% if days in range(0, 8) %}rgba(244, 67, 54, 0.2){% else %}rgba(128, 128, 128, 0.2){% endif %} !important;
      }
```

RGB Colors:
- Red: `rgb(244, 67, 54)`
- Yellow: `rgb(255, 235, 59)` 
- Green: `rgb(76, 175, 80)`
- Grey: `rgb(128, 128, 128)`

---

## Step 5: Full Working Example with card-mod

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
            primary_info: name
            secondary_info: state
            tap_action:
              action: more-info
            card_mod:
              style: |
                mushroom-shape-icon {
                  {% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
                  --icon-color: {% if days in range(0, 8) %}rgb(244, 67, 54){% else %}rgb(128, 128, 128){% endif %} !important;
                  --shape-color: {% if days in range(0, 8) %}rgba(244, 67, 54, 0.2){% else %}rgba(128, 128, 128, 0.2){% endif %} !important;
                }
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_recycling
            name: Recycling
            icon: mdi:recycle
            primary_info: name
            secondary_info: state
            tap_action:
              action: more-info
            card_mod:
              style: |
                mushroom-shape-icon {
                  {% set days = state_attr('sensor.ryde_waste_collection_recycling', 'days_until') | int(-1) %}
                  --icon-color: {% if days in range(0, 8) %}rgb(255, 235, 59){% else %}rgb(128, 128, 128){% endif %} !important;
                  --shape-color: {% if days in range(0, 8) %}rgba(255, 235, 59, 0.2){% else %}rgba(128, 128, 128, 0.2){% endif %} !important;
                }
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_garden_organics
            name: Garden Organics
            icon: mdi:leaf
            primary_info: name
            secondary_info: state
            tap_action:
              action: more-info
            card_mod:
              style: |
                mushroom-shape-icon {
                  {% set days = state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') | int(-1) %}
                  --icon-color: {% if days in range(0, 8) %}rgb(76, 175, 80){% else %}rgb(128, 128, 128){% endif %} !important;
                  --shape-color: {% if days in range(0, 8) %}rgba(76, 175, 80, 0.2){% else %}rgba(128, 128, 128, 0.2){% endif %} !important;
                }
```

---

## Diagnosis Summary

**If Step 1 (static color) doesn't work:**
- Mushroom not installed or loaded correctly
- Check HACS → Frontend → Mushroom
- Try reinstalling Mushroom

**If Step 1 works but Step 2 (template) doesn't:**
- Your Mushroom version doesn't support `icon_color` templates
- Update to v2.0.0+
- OR use card-mod approach (Step 5)

**If Steps 1 & 2 work but your original template doesn't:**
- Template syntax issue (unlikely since it evaluates correctly)
- Try the exact template from this doc

**card-mod is the most reliable solution** if Mushroom templates aren't working.
