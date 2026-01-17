# Visual Dashboard Example

## What Your Home Assistant Dashboard Will Look Like

```
╔═══════════════════════════════════════════════════════╗
║                  Waste Collection                     ║
║             Ryde Council - Next Collections           ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  🗑️  General Waste                          🔴 🔔    ║
║      Wed 21/1/2026 (4 days)                          ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  ♻️  Recycling                               🟡 🔔    ║
║      Wed 21/1/2026 (4 days)                          ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  🍃  Garden Organics                         ⚫       ║
║      Wed 28/1/2026 (11 days)                         ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  📅  Next: General Waste in 4 days                    ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

## Color Indicator Behavior

### Within 7 Days (Upcoming)
- **General Waste** → 🔴 Red indicator + 🔔 Bell badge
- **Recycling** → 🟡 Yellow indicator + 🔔 Bell badge  
- **Garden Organics** → 🟢 Green indicator + 🔔 Bell badge

### More Than 7 Days Away
- All types → ⚫ Grey indicator (no bell)

## Example States

### Scenario 1: Multiple Collections This Week
```
🗑️  General Waste       🔴 🔔
    Mon 20/1/2026 (3 days)

♻️  Recycling            🟡 🔔
    Mon 20/1/2026 (3 days)

🍃  Garden Organics     🟢 🔔
    Wed 22/1/2026 (5 days)

📅 Next: General Waste in 3 days
```

### Scenario 2: One Collection Upcoming
```
🗑️  General Waste       🔴 🔔
    Tue 21/1/2026 (4 days)

♻️  Recycling            ⚫
    Tue 28/1/2026 (11 days)

🍃  Garden Organics     ⚫
    Wed 29/1/2026 (12 days)

📅 Next: General Waste in 4 days
```

### Scenario 3: No Collections Soon
```
🗑️  General Waste       ⚫
    Wed 29/1/2026 (12 days)

♻️  Recycling            ⚫
    Wed 29/1/2026 (12 days)

🍃  Garden Organics     ⚫
    Wed 5/2/2026 (19 days)

📅 Next: General Waste in 12 days
```

## Mobile View

On mobile devices, the cards stack vertically and remain fully functional:

```
┌─────────────────────────┐
│  Waste Collection       │
│  Ryde Council           │
├─────────────────────────┤
│ 🗑️ General Waste   🔴🔔│
│ Wed 21/1/2026 (4 days)  │
├─────────────────────────┤
│ ♻️ Recycling         🟡🔔│
│ Wed 21/1/2026 (4 days)  │
├─────────────────────────┤
│ 🍃 Garden Organics  ⚫  │
│ Wed 28/1/2026 (11 days) │
├─────────────────────────┤
│ 📅 Next: General Waste  │
│    in 4 days            │
└─────────────────────────┘
```

## Tap Actions

Tapping any card opens the detailed sensor information showing:
- Full collection date
- Days until collection
- Collection type
- Last updated timestamp
- All sensor attributes

## Notification Example

When a collection is tomorrow (at 6 PM by default):

```
┌─────────────────────────────────┐
│ 🔔 Bins Tomorrow!               │
├─────────────────────────────────┤
│ Remember to put out:            │
│ General Waste, Recycling        │
└─────────────────────────────────┘
```

## Sensor Data Structure

### sensor.waste_general
```yaml
state: "Wed 21/1/2026"
attributes:
  friendly_name: General Waste Collection
  icon: mdi:trash-can
  date: "2026-01-21"
  days_until: 4
  collection_type: "General Waste"
  color: "red"
  upcoming: true
  last_updated: "2026-01-17T07:00:00"
```

### sensor.waste_recycling
```yaml
state: "Wed 21/1/2026"
attributes:
  friendly_name: Recycling Collection
  icon: mdi:recycle
  date: "2026-01-21"
  days_until: 4
  collection_type: "Recycling"
  color: "yellow"
  upcoming: true
  last_updated: "2026-01-17T07:00:00"
```

### sensor.waste_garden
```yaml
state: "Wed 28/1/2026"
attributes:
  friendly_name: Garden Organics Collection
  icon: mdi:leaf
  date: "2026-01-28"
  days_until: 11
  collection_type: "Garden Organics"
  color: "green"
  upcoming: false
  last_updated: "2026-01-17T07:00:00"
```

---

The Mushroom cards provide a clean, modern interface that's both functional and beautiful!
