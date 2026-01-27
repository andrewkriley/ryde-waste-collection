# Installation Guide

This guide covers both installation methods for the Ryde Waste Collection integration.

## Table of Contents
- [Option 1: Native Home Assistant Integration (Recommended)](#option-1-native-home-assistant-integration-recommended)
- [Option 2: Docker with MQTT](#option-2-docker-with-mqtt)
- [Comparison](#comparison)

---

## Option 1: Native Home Assistant Integration (Recommended)

The custom integration runs directly within Home Assistant - no Docker or MQTT broker required!

### Prerequisites
- Home Assistant 2024.1.0 or newer
- Access to your Home Assistant configuration directory

### Installation Methods

#### Method A: HACS (Easiest)

1. **Install HACS** (if not already installed)
   - Follow instructions at https://hacs.xyz/docs/setup/download

2. **Add Custom Repository**
   - Open HACS in Home Assistant
   - Click the three dots menu (top right)
   - Select "Custom repositories"
   - Add this repository URL: `https://github.com/andrewkriley/ryde-waste-collection-homeassistant`
   - Select category: "Integration"
   - Click "Add"

3. **Install Integration**
   - Find "Ryde Waste Collection" in HACS
   - Click "Download"
   - Restart Home Assistant

4. **Configure**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Ryde Waste Collection"
   - Enter your Ryde Council address (e.g., "129 Blaxland Road, Ryde")
   - Click "Submit"

#### Method B: Manual Installation

1. **Download Integration**
   ```bash
   cd /config  # or wherever your Home Assistant config is located
   mkdir -p custom_components
   cd custom_components
   git clone https://github.com/andrewkriley/ryde-waste-collection-homeassistant.git temp
   mv temp/custom_components/ryde_waste_collection .
   rm -rf temp
   ```

   Or manually download and extract the `custom_components/ryde_waste_collection` folder to your Home Assistant `custom_components` directory.

2. **Restart Home Assistant**

3. **Configure** (same as HACS method above)

### Configuration Options

After installation, you can configure:
- **Update Interval**: How often to check for new data (default: 12 hours)
  - Go to Settings → Devices & Services → Ryde Waste Collection
  - Click "Configure"
  - Adjust scan interval (1-24 hours)

### Sensor Entities

The integration creates three sensor entities:
- `sensor.ryde_waste_collection_general_waste`
- `sensor.ryde_waste_collection_recycling`
- `sensor.ryde_waste_collection_garden_organics`

Each sensor provides:
- **State**: Next collection date (e.g., "Tue 27/1/2026")
- **Attributes**:
  - `days_until`: Days until next collection
  - `collection_date`: Full collection date string
  - `address`: Your normalized address
  - `geolocation_id`: Ryde Council geolocation ID
  - `last_updated`: Last update timestamp

---

## Option 2: Docker with MQTT

Use this method if you prefer running as a separate Docker container with MQTT integration.

### Prerequisites
- Docker and Docker Compose installed
- MQTT broker (e.g., Mosquitto) running
- Home Assistant with MQTT integration configured

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/andrewkriley/ryde-waste-collection-homeassistant.git
   cd ryde-waste-collection-homeassistant
   ```

2. **Create Environment File**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your details:
   ```env
   RYDE_ADDRESS=129 Blaxland Road, Ryde
   MQTT_BROKER=your-mqtt-broker-ip
   MQTT_PORT=1883
   MQTT_USER=your-mqtt-username
   MQTT_PASSWORD=your-mqtt-password
   MQTT_TOPIC_PREFIX=ryde_waste
   UPDATE_INTERVAL=86400
   TZ=Australia/Sydney
   ```

3. **Start Container**
   ```bash
   docker compose up -d
   ```

4. **Verify**
   ```bash
   docker compose logs -f
   ```

   You should see sensors being published to MQTT.

### MQTT Sensor Entities

The Docker method creates three MQTT sensors via autodiscovery:
- `sensor.ryde_waste_general`
- `sensor.ryde_waste_recycling`
- `sensor.ryde_waste_garden`

See [MQTT.md](MQTT.md) for detailed MQTT configuration.

---

## Comparison

| Feature | Native Integration | Docker/MQTT |
|---------|-------------------|-------------|
| **Installation** | Simple (HACS or manual copy) | Requires Docker setup |
| **Dependencies** | None (built into HA) | Docker, MQTT broker |
| **Configuration** | UI-based config flow | Environment variables |
| **Resource Usage** | Minimal (runs in HA) | Separate container |
| **Updates** | Via HACS or manual | Docker image pull |
| **Multiple Addresses** | Yes (add multiple integrations) | One per container |
| **Recommended For** | Most users | Advanced setups, existing MQTT infrastructure |

---

## Troubleshooting

### Native Integration

**Integration doesn't appear in Add Integration**
- Ensure you've restarted Home Assistant after installation
- Check `config/custom_components/ryde_waste_collection/` exists
- Check Home Assistant logs for errors

**Address not found**
- Verify your address is in Ryde Council area
- Try variations (e.g., "123 Main St, Ryde" vs "123 Main Street, Ryde")
- Test address at https://www.ryde.nsw.gov.au/Environment-and-Waste/Waste-and-Recycling

**Sensors not updating**
- Check the coordinator update interval in integration options
- View integration logs: Settings → System → Logs (filter for "ryde_waste")

### Docker/MQTT

**Container exits immediately**
- Check logs: `docker compose logs`
- Verify MQTT credentials are correct
- Ensure address is valid

**Sensors not appearing in Home Assistant**
- Verify MQTT integration is configured in HA
- Check MQTT broker logs
- Confirm autodiscovery is enabled in HA MQTT integration

---

## Uninstallation

### Native Integration
1. Go to Settings → Devices & Services
2. Find "Ryde Waste Collection"
3. Click three dots → "Delete"
4. (Optional) Remove from `custom_components` folder

### Docker/MQTT
```bash
docker compose down
docker rmi andrewkriley/ryde-waste-collection:latest
```

---

## Support

- **Issues**: https://github.com/andrewkriley/ryde-waste-collection-homeassistant/issues
- **Discussions**: https://github.com/andrewkriley/ryde-waste-collection-homeassistant/discussions
