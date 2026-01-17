# Home Assistant Integration - Quick Start

## What You Get

✨ **Beautiful Dashboard** with color-coded waste collection indicators:
- 🔴 **Red** for General Waste
- 🟡 **Yellow** for Recycling  
- 🟢 **Green** for Garden Organics

💡 Indicators light up only when collection is within 7 days!

## Quick Setup (3 Steps)

### 1. Get Your Home Assistant Token

In Home Assistant:
- Click your profile → "Long-Lived Access Tokens" → "Create Token"
- Copy the token

### 2. Test the Integration

```bash
/tmp/ryde_env/bin/python ryde_to_homeassistant.py \
  "YOUR_ADDRESS" \
  --ha-url "http://homeassistant.local:8123" \
  --ha-token "YOUR_TOKEN_HERE"
```

You should see:
```
✓ Published General Waste: Wed 21/1/2026 (in 4 days)
✓ Published Recycling: Wed 21/1/2026 (in 4 days)
✓ Published Garden Organics: Wed 28/1/2026 (in 11 days)
```

### 3. Add the Dashboard Card

1. Edit your Home Assistant dashboard
2. Add a new card (Manual mode)
3. Copy/paste from `homeassistant_mushroom_card.yaml`
4. Save!

## Make It Automatic

Add to Home Assistant `configuration.yaml`:

```yaml
shell_command:
  update_ryde_waste: >
    /tmp/ryde_env/bin/python /home/andreril/ryde-waste-collection/ryde_to_homeassistant.py 
    "YOUR_ADDRESS" 
    --ha-url "http://homeassistant.local:8123" 
    --ha-token "YOUR_TOKEN_HERE"

automation:
  - alias: Update Ryde Waste Collection
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: shell_command.update_ryde_waste
```

## What Gets Created

Three sensors in Home Assistant:
- `sensor.waste_general` - General Waste collection
- `sensor.waste_recycling` - Recycling collection
- `sensor.waste_garden` - Garden Organics collection

Each sensor includes:
- Collection date
- Days until collection
- Whether it's upcoming (within 7 days)
- Color coding

## Files You Need

1. **`ryde_to_homeassistant.py`** - Integration script ✅
2. **`homeassistant_mushroom_card.yaml`** - Dashboard card config ✅
3. **`homeassistant_automation.yaml`** - Automation examples ✅
4. **`publish-to-homeassistant.sh`** - Wrapper script ✅

## Need More Help?

Read the full guide: **`HOMEASSISTANT_SETUP.md`**

See visual examples: **`VISUAL_EXAMPLE.md`**

## One-Line Test

```bash
export HA_TOKEN="your_token" && \
./publish-to-homeassistant.sh
```

---

That's it! Your waste collection dashboard is ready! 🎉
