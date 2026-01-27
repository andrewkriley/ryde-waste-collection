# Customization Guide

## Colored Icons

Home Assistant sensors don't support icon colors in the entity definition, but you can easily add colored icons using entity customization.

### Method 1: Using customize.yaml (Recommended)

Add this to your `configuration.yaml`:

```yaml
homeassistant:
  customize: !include customize.yaml
```

Then create/edit `customize.yaml`:

```yaml
# Ryde Waste Collection - Colored Icons
sensor.ryde_waste_collection_general_waste:
  icon_color: red
  
sensor.ryde_waste_collection_recycling:
  icon_color: yellow
  
sensor.ryde_waste_collection_garden_organics:
  icon_color: green
```

### Method 2: Using Mushroom Cards

Mushroom cards support icon colors directly:

```yaml
type: custom:mushroom-chips-card
chips:
  - type: entity
    entity: sensor.ryde_waste_collection_general_waste
    icon: mdi:trash-can
    icon_color: red
    content_info: name
    
  - type: entity
    entity: sensor.ryde_waste_collection_recycling
    icon: mdi:recycle
    icon_color: yellow
    content_info: name
    
  - type: entity
    entity: sensor.ryde_waste_collection_garden_organics
    icon: mdi:leaf
    icon_color: green
    content_info: name
```

### Method 3: Using Custom Button Card

```yaml
type: custom:button-card
entity: sensor.ryde_waste_collection_general_waste
name: General Waste
icon: mdi:trash-can
color: red
show_state: true
state:
  - value: ".*"
    styles:
      icon:
        - color: red
```

### Method 4: Using card-mod

If you're using regular entity cards, you can use card-mod:

```yaml
type: entities
entities:
  - entity: sensor.ryde_waste_collection_general_waste
    card_mod:
      style: |
        :host {
          --card-mod-icon-color: red;
        }
        
  - entity: sensor.ryde_waste_collection_recycling
    card_mod:
      style: |
        :host {
          --card-mod-icon-color: yellow;
        }
        
  - entity: sensor.ryde_waste_collection_garden_organics
    card_mod:
      style: |
        :host {
          --card-mod-icon-color: green;
        }
```

## Complete Dashboard Example

Here's a complete example using Mushroom cards with colors:

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Waste Collection
    subtitle: Next Collection Dates
    
  - type: custom:mushroom-chips-card
    alignment: center
    chips:
      - type: entity
        entity: sensor.ryde_waste_collection_general_waste
        icon: mdi:trash-can
        icon_color: red
        tap_action:
          action: more-info
        
      - type: entity
        entity: sensor.ryde_waste_collection_recycling
        icon: mdi:recycle
        icon_color: yellow
        tap_action:
          action: more-info
        
      - type: entity
        entity: sensor.ryde_waste_collection_garden_organics
        icon: mdi:leaf
        icon_color: green
        tap_action:
          action: more-info
  
  - type: custom:mushroom-entity-card
    entity: sensor.ryde_waste_collection_general_waste
    name: General Waste
    icon: mdi:trash-can
    icon_color: red
    primary_info: name
    secondary_info: state
    badge_color: red
    badge_icon: mdi:calendar
    
  - type: custom:mushroom-entity-card
    entity: sensor.ryde_waste_collection_recycling
    name: Recycling
    icon: mdi:recycle
    icon_color: yellow
    primary_info: name
    secondary_info: state
    badge_color: yellow
    badge_icon: mdi:calendar
    
  - type: custom:mushroom-entity-card
    entity: sensor.ryde_waste_collection_garden_organics
    name: Garden Organics
    icon: mdi:leaf
    icon_color: green
    primary_info: name
    secondary_info: state
    badge_color: green
    badge_icon: mdi:calendar
```

## Dynamic Icon Colors Based on Days Until Collection

You can also make the icon color change based on how soon the collection is:

```yaml
type: custom:button-card
entity: sensor.ryde_waste_collection_general_waste
name: General Waste
icon: mdi:trash-can
show_state: true
state:
  - value: ".*"
    operator: template
    color: |
      [[[
        const days = entity.attributes.days_until;
        if (days === 0) return 'red';
        if (days === 1) return 'orange';
        if (days <= 3) return 'yellow';
        return 'green';
      ]]]
styles:
  icon:
    - color: |
        [[[
          const days = entity.attributes.days_until;
          if (days === 0) return 'red';
          if (days === 1) return 'orange';
          if (days <= 3) return 'yellow';
          return 'green';
        ]]]
```

## Required Custom Cards

Most colorization methods require custom cards. Install via HACS:

- **Mushroom Cards**: `HACS → Frontend → Mushroom`
- **Button Card**: `HACS → Frontend → button-card`
- **card-mod**: `HACS → Frontend → card-mod`

## Color Recommendations

- 🔴 **Red**: General Waste (red bin)
- 🟡 **Yellow**: Recycling (yellow bin)
- 🟢 **Green**: Garden Organics (green bin)

These colors match the actual bin colors used by Ryde Council!
