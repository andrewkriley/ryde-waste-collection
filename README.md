# Ryde Waste Collection - Home Assistant Custom Integration

[![GitHub Release](https://img.shields.io/github/release/andrewkriley/ryde-waste-collection-homeassistant.svg?style=flat-square)](https://github.com/andrewkriley/ryde-waste-collection-homeassistant/releases)
[![License](https://img.shields.io/github/license/andrewkriley/ryde-waste-collection-homeassistant.svg?style=flat-square)](LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/custom-components/hacs)

**Unofficial Home Assistant integration for tracking Ryde Council waste collection schedules.**

*Created by Andrew Riley - Not affiliated with or endorsed by Ryde Council.*

---

## ⚠️ Disclaimer

This is an **unofficial** integration created by Andrew Riley. It is **not affiliated with, endorsed by, or in any way officially connected** with the City of Ryde Council. This integration uses publicly accessible data from the Ryde Council website.

- **Data Source**: Ryde Council public APIs
- **Author**: Andrew Riley
- **Support**: Community-driven (not official Ryde Council support)

---

## ✨ Features

- 🗑️ **Three Waste Types**: General Waste, Recycling, and Garden Organics
- 📅 **Next Collection Dates**: Always know when to put your bins out
- ⏰ **Days Until Collection**: Count down to collection day
- 🎨 **Colored Icons**: Match your dashboard to bin colors (red, yellow, green)
- ⚙️ **Easy Setup**: UI-based configuration - just enter your address
- 🔄 **Configurable Updates**: Set your own update interval (1-24 hours)
- 📍 **Multiple Addresses**: Add as many addresses as you need

## 🚀 Quick Start

### Installation

#### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu (top right) → Custom repositories
3. Add: `https://github.com/andrewkriley/ryde-waste-collection-homeassistant`
4. Category: Integration
5. Click "Download" and restart Home Assistant

#### Manual Installation

```bash
cd /path/to/homeassistant/custom_components
git clone https://github.com/andrewkriley/ryde-waste-collection-homeassistant.git ryde_waste_collection
```

Restart Home Assistant after installation.

### Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Ryde Waste Collection"**
4. Enter your Ryde LGA address (e.g., "129 Blaxland Road, Ryde")
5. Click **Submit**

**Note**: During setup, you'll see a disclaimer that this is an unofficial integration.

## 📊 Sensor Entities

The integration creates three sensors:

- `sensor.ryde_waste_collection_general_waste`
- `sensor.ryde_waste_collection_recycling`
- `sensor.ryde_waste_collection_garden_organics`

### Sensor Attributes

Each sensor includes:
- **State**: Next collection date (e.g., "Tue 27/1/2026")
- **days_until**: Days until collection
- **collection_date**: Full date string
- **address**: Your normalized Ryde Council address
- **geolocation_id**: Ryde Council geolocation ID
- **last_updated**: Last update timestamp

## 🎨 Customization

### Colored Icons

See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for dynamic icon colors:
- Icons turn color when collection is within 7 days
- Stay grey/blue when more than 7 days away
- Match actual bin colors: Red, Yellow, Green

### Dashboard Examples

Check out [docs/DASHBOARD_SETUP.md](docs/DASHBOARD_SETUP.md) for:
- Mushroom card configurations
- Entity card examples
- Complete dashboard layouts

## 📖 Documentation

- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Customization Guide](docs/CUSTOMIZATION.md)** - Colored icons and styling
- **[Dashboard Setup](docs/DASHBOARD_SETUP.md)** - Card configurations
- **[API Documentation](docs/API_VALIDATION.md)** - Technical details
- **[Contributing](CONTRIBUTING.md)** - How to contribute

## 🛠️ Development

### Project Structure

```
ryde-waste-collection-homeassistant/
├── __init__.py              # Integration entry point
├── config_flow.py           # UI configuration
├── coordinator.py           # Data fetching
├── sensor.py                # Sensor entities
├── const.py                 # Constants
├── manifest.json            # Integration metadata
├── strings.json             # UI strings
├── translations/            # Translations
├── docs/                    # Documentation
└── .github/                 # GitHub workflows
```

### Running Locally

1. Clone the repository
2. Create a symbolic link in your HA custom_components:
   ```bash
   ln -s /path/to/ryde-waste-collection-homeassistant /path/to/homeassistant/custom_components/ryde_waste_collection
   ```
3. Restart Home Assistant
4. Configure via UI

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Credits

- **Author**: Andrew Riley
- **Data Source**: Ryde Council public APIs
- **Community**: Home Assistant community for integration frameworks
- **Contributors**: All contributors and users

## 💬 Support

- 🐛 [Report an Issue](https://github.com/andrewkriley/ryde-waste-collection-homeassistant/issues)
- 💬 [Discussions](https://github.com/andrewkriley/ryde-waste-collection-homeassistant/discussions)
- ⭐ Star this repo if you find it useful!

---

## ⚠️ Important Notes

- **Unofficial**: This integration is not affiliated with or endorsed by Ryde Council
- **Data Accuracy**: While we strive for accuracy, always verify collection dates on the official Ryde Council website
- **No Warranty**: Provided as-is with no guarantees
- **Community Support**: Support is community-driven, not from Ryde Council
- **API Changes**: Integration may break if Ryde Council changes their APIs

---

**Disclaimer**: This is an unofficial, community-created integration. It is not affiliated with, endorsed by, or in any way officially connected with the City of Ryde Council.
