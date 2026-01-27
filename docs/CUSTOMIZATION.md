# Customization Guide

## Dynamic Icon Colors

Make your waste collection icons change color automatically as collection day approaches!

### Overview

Icons will:
- **Stay grey/blue** (default) when collection is more than 7 days away
- **Turn to bin color** when collection is within 7 days
- Match actual Ryde Council bin colors: 🔴 Red (General), 🟡 Yellow (Recycling), 🟢 Green (Garden)

This helps you quickly see which bins need attention soon!

---

## Method 1: Mushroom Cards (Recommended)

Mushroom cards are the easiest way to add dynamic colors. Install via HACS: **Frontend → Mushroom**

### Individual Cards

```yaml
type: custom:mushroom-entity-card
entity: sensor.ryde_waste_collection_general_waste
name: General Waste
icon: mdi:trash-can
icon_color: |-
  {% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 7 %}
    red
  {% else %}
    grey
  {% endif %}
primary_info: name
secondary_info: state
```

```yaml
type: custom:mushroom-entity-card
entity: sensor.ryde_waste_collection_recycling
name: Recycling
icon: mdi:recycle
icon_color: |-
  {% if state_attr('sensor.ryde_waste_collection_recycling', 'days_until') <= 7 %}
    yellow
  {% else %}
    grey
  {% endif %}
primary_info: name
secondary_info: state
```

```yaml
type: custom:mushroom-entity-card
entity: sensor.ryde_waste_collection_garden_organics
name: Garden Organics
icon: mdi:leaf
icon_color: |-
  {% if state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') <= 7 %}
    green
  {% else %}
    grey
  {% endif %}
primary_info: name
secondary_info: state
```

### Compact Chips (Horizontal Layout)

```yaml
type: custom:mushroom-chips-card
alignment: center
chips:
  - type: template
    entity: sensor.ryde_waste_collection_general_waste
    icon: mdi:trash-can
    icon_color: |-
      {% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 7 %}
        red
      {% else %}
        grey
      {% endif %}
    content: |
      {{ states('sensor.ryde_waste_collection_general_waste') }}
    tap_action:
      action: more-info
      
  - type: template
    entity: sensor.ryde_waste_collection_recycling
    icon: mdi:recycle
    icon_color: |-
      {% if state_attr('sensor.ryde_waste_collection_recycling', 'days_until') <= 7 %}
        yellow
      {% else %}
        grey
      {% endif %}
    content: |
      {{ states('sensor.ryde_waste_collection_recycling') }}
    tap_action:
      action: more-info
      
  - type: template
    entity: sensor.ryde_waste_collection_garden_organics
    icon: mdi:leaf
    icon_color: |-
      {% if state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') <= 7 %}
        green
      {% else %}
        grey
      {% endif %}
    content: |
      {{ states('sensor.ryde_waste_collection_garden_organics') }}
    tap_action:
      action: more-info
```

---

## Method 2: Custom Button Card

Install via HACS: **Frontend → button-card**

```yaml
type: custom:button-card
entity: sensor.ryde_waste_collection_general_waste
name: General Waste
icon: mdi:trash-can
show_state: true
show_last_changed: true
styles:
  icon:
    - color: |
        [[[
          const days = entity.attributes.days_until;
          if (days <= 7) return 'red';
          return 'var(--primary-text-color)';
        ]]]
  card:
    - padding: 10px
```

```yaml
type: custom:button-card
entity: sensor.ryde_waste_collection_recycling
name: Recycling
icon: mdi:recycle
show_state: true
show_last_changed: true
styles:
  icon:
    - color: |
        [[[
          const days = entity.attributes.days_until;
          if (days <= 7) return 'gold';
          return 'var(--primary-text-color)';
        ]]]
  card:
    - padding: 10px
```

```yaml
type: custom:button-card
entity: sensor.ryde_waste_collection_garden_organics
name: Garden Organics
icon: mdi:leaf
show_state: true
show_last_changed: true
styles:
  icon:
    - color: |
        [[[
          const days = entity.attributes.days_until;
          if (days <= 7) return 'green';
          return 'var(--primary-text-color)';
        ]]]
  card:
    - padding: 10px
```

---

## Method 3: Card-mod (Works with Standard Cards)

Install via HACS: **Frontend → card-mod**

```yaml
type: entities
entities:
  - entity: sensor.ryde_waste_collection_general_waste
    card_mod:
      style: |
        :host {
          --card-mod-icon-color: 
            {% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 7 %}
              red
            {% else %}
              var(--primary-text-color)
            {% endif %};
        }
        
  - entity: sensor.ryde_waste_collection_recycling
    card_mod:
      style: |
        :host {
          --card-mod-icon-color: 
            {% if state_attr('sensor.ryde_waste_collection_recycling', 'days_until') <= 7 %}
              gold
            {% else %}
              var(--primary-text-color)
            {% endif %};
        }
        
  - entity: sensor.ryde_waste_collection_garden_organics
    card_mod:
      style: |
        :host {
          --card-mod-icon-color: 
            {% if state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') <= 7 %}
              green
            {% else %}
              var(--primary-text-color)
            {% endif %};
        }
```

---

## Complete Dashboard Example

Here's a complete vertical stack with dynamic colors using Mushroom cards:

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Waste Collection
    subtitle: Next 7 Days
    
  - type: custom:mushroom-entity-card
    entity: sensor.ryde_waste_collection_general_waste
    name: General Waste
    icon: mdi:trash-can
    icon_color: |-
      {% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 7 %}
        red
      {% else %}
        grey
      {% endif %}
    primary_info: name
    secondary_info: state
    badge_icon: |-
      {% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 1 %}
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
      {% if state_attr('sensor.ryde_waste_collection_recycling', 'days_until') <= 7 %}
        yellow
      {% else %}
        grey
      {% endif %}
    primary_info: name
    secondary_info: state
    badge_icon: |-
      {% if state_attr('sensor.ryde_waste_collection_recycling', 'days_until') <= 1 %}
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
      {% if state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') <= 7 %}
        green
      {% else %}
        grey
      {% endif %}
    primary_info: name
    secondary_info: state
    badge_icon: |-
      {% if state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') <= 1 %}
        mdi:alert
      {% endif %}
    badge_color: green
    tap_action:
      action: more-info
```

---

## Customizing the Threshold

Want to change when icons become colored? Just change the `7` to any number of days:

```yaml
{% if state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') <= 3 %}
  red
{% else %}
  grey
{% endif %}
```

Common thresholds:
- **3 days**: Only color when very soon
- **7 days**: Color when within a week (recommended)
- **14 days**: Color when within two weeks

---

## Color Reference

Matching actual Ryde Council bin colors:

| Waste Type | Icon Color | Default Color | Days Until |
|------------|------------|---------------|------------|
| General Waste | `red` | `grey` | ≤ 7 days |
| Recycling | `yellow` | `grey` | ≤ 7 days |
| Garden Organics | `green` | `grey` | ≤ 7 days |

**Bonus**: Add alert badges when collection is tomorrow or today!

---

## Installing Required Cards

All these methods require custom cards from HACS:

1. Open **HACS** in Home Assistant
2. Go to **Frontend**
3. Search and install:
   - **Mushroom** (easiest, recommended)
   - **button-card** (advanced styling)
   - **card-mod** (works with standard cards)
4. Restart Home Assistant
5. Add the card configurations above

---

## Why Dynamic Colors?

- **At a glance**: Quickly see which bins are due soon
- **Less clutter**: Icons only stand out when relevant
- **Smart reminders**: Visual cue without notifications
- **Customizable**: Adjust the threshold to your preference

The icons will automatically update as collection day approaches!
