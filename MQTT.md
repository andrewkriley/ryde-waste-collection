# MQTT Integration Guide

This guide covers the MQTT-based deployment which is the **recommended approach** for containerized environments.

## Why MQTT?

✅ **Benefits over REST API:**
- Container runs independently - no Home Assistant automations needed
- More reliable - built-in reconnection and retry logic
- Auto-discovery - sensors appear automatically in Home Assistant
- Better performance - container handles all scraping internally
- Cleaner architecture - separation of concerns

## Prerequisites

1. **MQTT Broker** - Usually built into Home Assistant or Mosquitto
2. **Home Assistant MQTT Integration** - Configured and working
3. **MQTT Discovery** - Enabled (default in Home Assistant)

## Quick Start

### 1. Enable MQTT in Home Assistant

If not already enabled:

1. Go to Settings → Devices & Services
2. Add Integration → MQTT
3. Configure your broker (usually `localhost` if using built-in broker)

Verify MQTT is working in `configuration.yaml`:
```yaml
mqtt:
  discovery: true  # This should be enabled (default)
  discovery_prefix: homeassistant
```

### 2. Configure the Container

Edit `.env`:

```env
# Required
RYDE_ADDRESS="Your Street Address, Ryde"
MQTT_BROKER="homeassistant.local"  # or your HA IP

# Optional - if MQTT requires authentication
MQTT_USER="mqtt_user"
MQTT_PASSWORD="mqtt_password"
```

### 3. Start the Container

```bash
docker-compose up -d
```

### 4. Verify Sensors

Within a minute, check Home Assistant:
- Settings → Devices & Services → MQTT
- Look for "Ryde Waste Collection" device
- Three sensors should appear automatically

## MQTT Configuration Options

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `RYDE_ADDRESS` | Your address | `"123 Main St, Ryde"` |
| `MQTT_BROKER` | Broker hostname/IP | `"homeassistant.local"` or `"192.168.1.100"` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTT_PORT` | `1883` | Broker port (8883 for TLS) |
| `MQTT_USER` | (none) | MQTT username |
| `MQTT_PASSWORD` | (none) | MQTT password |
| `MQTT_TOPIC_PREFIX` | `ryde_waste` | Topic prefix for all sensors |

## MQTT Topics

The container publishes to these topics:

### Discovery (Auto-registration)
```
homeassistant/sensor/ryde_waste_general/config
homeassistant/sensor/ryde_waste_recycling/config
homeassistant/sensor/ryde_waste_garden/config
```

### State Topics
```
ryde_waste/ryde_waste_general/state
ryde_waste/ryde_waste_recycling/state
ryde_waste/ryde_waste_garden/state
```

### Attributes Topics
```
ryde_waste/ryde_waste_general/attributes
ryde_waste/ryde_waste_recycling/attributes
ryde_waste/ryde_waste_garden/attributes
```

## MQTT Discovery Payload

Example discovery payload for General Waste:

```json
{
  "name": "General Waste Collection",
  "unique_id": "ryde_waste_general",
  "state_topic": "ryde_waste/ryde_waste_general/state",
  "json_attributes_topic": "ryde_waste/ryde_waste_general/attributes",
  "icon": "mdi:trash-can",
  "device": {
    "identifiers": ["ryde_waste_collection"],
    "name": "Ryde Waste Collection",
    "model": "Waste Collection Monitor",
    "manufacturer": "Ryde Council Scraper"
  }
}
```

## Sensor Attributes

Each sensor includes these attributes:

```json
{
  "friendly_name": "General Waste Collection",
  "icon": "mdi:trash-can",
  "date": "2026-01-21",
  "date_formatted": "Wed 21/1/2026",
  "days_until": 4,
  "collection_type": "General Waste",
  "color": "red",
  "upcoming": true,
  "last_updated": "2026-01-17T07:00:00"
}
```

## MQTT Authentication

### Option 1: No Authentication (Local Network)

If your MQTT broker doesn't require authentication:
```env
MQTT_BROKER="homeassistant.local"
MQTT_PORT=1883
```

### Option 2: Username/Password

Create an MQTT user in Home Assistant:
1. Settings → People → Users
2. Add user for MQTT access
3. Configure container:

```env
MQTT_BROKER="homeassistant.local"
MQTT_USER="mqtt_user"
MQTT_PASSWORD="your_secure_password"
```

### Option 3: TLS/SSL (Advanced)

For encrypted connections:
```env
MQTT_BROKER="homeassistant.local"
MQTT_PORT=8883
MQTT_USER="mqtt_user"
MQTT_PASSWORD="your_secure_password"
```

Note: TLS requires additional certificate configuration (not covered here).

## Troubleshooting

### Sensors not appearing

1. **Check MQTT integration**
   ```bash
   # In Home Assistant, check MQTT is enabled
   Settings → Devices & Services → MQTT
   ```

2. **Check container logs**
   ```bash
   docker-compose logs -f ryde-waste-collection
   ```

3. **Verify MQTT connection**
   Look for "✓ Connected to MQTT broker" in logs

4. **Check discovery is enabled**
   ```yaml
   # configuration.yaml
   mqtt:
     discovery: true
   ```

5. **Restart Home Assistant**
   Sometimes needed to pick up new MQTT devices

### Connection refused

- **Check MQTT broker is running**
  ```bash
  # Test from host
  mosquitto_sub -h homeassistant.local -t '#' -v
  ```

- **Check network connectivity**
  ```bash
  # From host
  ping homeassistant.local
  ```

- **Verify port is correct**
  - Default: 1883 (non-TLS)
  - TLS: 8883

### Authentication failed

- Verify MQTT user exists in Home Assistant
- Check credentials in `.env` are correct
- Ensure no extra spaces in username/password

### Data not updating

- Check container is running: `docker-compose ps`
- Check logs: `docker-compose logs -f`
- Verify update interval: `docker-compose config`

## Testing MQTT Manually

### Subscribe to all topics
```bash
# From host with mosquitto-clients installed
mosquitto_sub -h homeassistant.local -t 'ryde_waste/#' -v
```

### Test the scraper manually
```bash
docker-compose exec ryde-waste-collection \
  python /app/ryde_mqtt_publisher.py \
  "Your Address" \
  --mqtt-broker homeassistant.local \
  --mqtt-port 1883
```

## Comparison: MQTT vs REST API

| Feature | MQTT (Recommended) | REST API |
|---------|-------------------|----------|
| Setup | Minimal | Requires HA automation |
| Auto-discovery | ✅ Yes | ❌ No |
| Reconnection | ✅ Automatic | Manual |
| Container-friendly | ✅ Yes | Partial |
| Performance | ✅ Better | Good |
| Complexity | ✅ Simple | More complex |

## Advanced Configuration

### Custom Topic Prefix

```env
MQTT_TOPIC_PREFIX=my_custom_prefix
```

Topics become:
```
my_custom_prefix/ryde_waste_general/state
my_custom_prefix/ryde_waste_recycling/state
etc.
```

### Multiple Addresses

Run multiple containers with different prefixes:

```yaml
# docker-compose.yml
services:
  ryde-address-1:
    build: .
    environment:
      RYDE_ADDRESS: "123 Main St, Ryde"
      MQTT_TOPIC_PREFIX: "ryde_waste_address1"
      # ... other config
  
  ryde-address-2:
    build: .
    environment:
      RYDE_ADDRESS: "456 Oak Ave, Ryde"
      MQTT_TOPIC_PREFIX: "ryde_waste_address2"
      # ... other config
```

## Home Assistant Dashboard

The Mushroom cards work the same way with MQTT sensors!

Use the same `homeassistant_mushroom_card.yaml` - just ensure the sensor entity IDs match:
- `sensor.ryde_waste_general`
- `sensor.ryde_waste_recycling`
- `sensor.ryde_waste_garden`

## No Automations Needed!

Unlike the REST API approach, with MQTT you DON'T need any Home Assistant automations. The container:
- Runs autonomously
- Scrapes on schedule
- Publishes directly to MQTT
- Auto-registers sensors via discovery

## Summary

MQTT provides a **cleaner, more reliable** integration for containerized deployments. The container handles everything independently, and Home Assistant automatically discovers the sensors.

**Recommended for:**
- Docker deployments
- Home servers
- NAS devices
- Any containerized environment

---

**Next:** See [DOCKER.md](DOCKER.md) for full Docker deployment guide
