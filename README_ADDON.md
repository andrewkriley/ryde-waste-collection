# Ryde Waste Collection - Home Assistant Integration

Track your Ryde Council waste collection schedule directly in Home Assistant!

[![GitHub Release](https://img.shields.io/github/release/andrewkriley/ryde-waste-collection-homeassistant.svg?style=flat-square)](https://github.com/andrewkriley/ryde-waste-collection-homeassistant/releases)
[![License](https://img.shields.io/github/license/andrewkriley/ryde-waste-collection-homeassistant.svg?style=flat-square)](LICENSE)

## Features

✨ **Two Installation Options:**
- **Native Home Assistant Integration** (Recommended) - Runs directly in HA, no external dependencies
- **Docker with MQTT** - For advanced users with existing MQTT infrastructure

🗑️ **Track Three Waste Types:**
- General Waste
- Recycling
- Garden Organics

📊 **Rich Data:**
- Next collection date
- Days until collection
- Formatted dates with day of week
- Normalized address from Ryde Council

⚙️ **Easy Configuration:**
- UI-based setup (native integration)
- Configurable update intervals
- Multiple addresses supported

## Quick Start

### Option 1: Native Integration (Recommended)

**Via HACS:**
1. Add this repo as a custom repository in HACS
2. Install "Ryde Waste Collection"
3. Restart Home Assistant
4. Add integration via UI: Settings → Devices & Services → Add Integration
5. Search "Ryde Waste Collection" and enter your address

**Manual:**
1. Copy `custom_components/ryde_waste_collection` to your HA config
2. Restart Home Assistant
3. Configure via UI

### Option 2: Docker with MQTT

```bash
git clone https://github.com/andrewkriley/ryde-waste-collection-homeassistant.git
cd ryde-waste-collection-homeassistant
cp .env.example .env
# Edit .env with your details
docker compose up -d
```

📖 **Full installation guide:** [INSTALLATION.md](INSTALLATION.md)

## Screenshots

### Native Integration Setup
<img src="docs/images/config_flow.png" width="400" alt="Config Flow">

### Sensor Entities
<img src="docs/images/sensors.png" width="400" alt="Sensor Entities">

### Dashboard Card
<img src="docs/images/dashboard.png" width="400" alt="Dashboard Card">

## Example Sensors

**Native Integration:**
- `sensor.ryde_waste_collection_general_waste`
- `sensor.ryde_waste_collection_recycling`
- `sensor.ryde_waste_collection_garden_organics`

**Docker/MQTT:**
- `sensor.ryde_waste_general`
- `sensor.ryde_waste_recycling`
- `sensor.ryde_waste_garden`

### Sensor Attributes

```yaml
state: "Tue 27/1/2026"
attributes:
  days_until: 0
  collection_date: "Tue 27/1/2026"
  address: "129 Blaxland Road, Ryde 2112"
  geolocation_id: "b148f7d7-e435-4b28-8970-b89af8be2ba0"
  last_updated: "2026-01-27T19:00:00"
```

## Dashboard Examples

See [DASHBOARD_SETUP.md](docs/DASHBOARD_SETUP.md) for Mushroom card configurations and other dashboard ideas.

## Documentation

- [Installation Guide](INSTALLATION.md) - Both installation methods
- [API Documentation](API_VALIDATION.md) - Technical details about the Ryde Council APIs
- [MQTT Setup](MQTT.md) - Docker/MQTT specific configuration
- [Dashboard Setup](docs/DASHBOARD_SETUP.md) - Card configurations
- [Docker Guide](DOCKER.md) - Docker-specific documentation

## Comparison: Native vs Docker

| Feature | Native Integration | Docker/MQTT |
|---------|-------------------|-------------|
| Setup Complexity | ⭐ Easy | ⭐⭐⭐ Advanced |
| Dependencies | None | Docker, MQTT |
| Resource Usage | Minimal | Moderate |
| Multiple Addresses | ✅ Yes | One per container |
| Updates | Via HACS | Docker pull |

**Recommendation:** Use the native integration unless you have specific requirements for Docker/MQTT.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

- Ryde Council for providing the public APIs
- Home Assistant community for integration frameworks
- Contributors and users for feedback and improvements

## Support

- 🐛 [Report an Issue](https://github.com/andrewkriley/ryde-waste-collection-homeassistant/issues)
- 💬 [Discussions](https://github.com/andrewkriley/ryde-waste-collection-homeassistant/discussions)
- ⭐ Star this repo if you find it useful!

---

**Note:** This is an unofficial integration and is not affiliated with Ryde Council.
