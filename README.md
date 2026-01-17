# Ryde Council Waste Collection Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated waste collection date scraper for Ryde Council (NSW, Australia) with Home Assistant integration via MQTT and beautiful Mushroom card dashboard.

![Ryde Waste Collection Dashboard](ryde-waste-collection-homeassistant.png)

![Home Assistant Dashboard](https://img.shields.io/badge/Home%20Assistant-Integration-blue)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Required-blue)

## ✨ Features

- 🐳 **Docker containerized** - Easy deployment and automatic updates
- 📡 **MQTT Discovery** - Sensors auto-register in Home Assistant
- 🎨 **Beautiful Mushroom cards** - Color-coded indicators (Red/Yellow/Green)
- 🚦 **Smart indicators** - Light up only when collection is within 7 days
- 🔄 **Automatic updates** - Configurable schedule (default: hourly)
- 🔔 **Optional notifications** - Get reminded about upcoming collections
- 🗑️ **Three waste types**:
  - 🔴 General Waste (Red)
  - 🟡 Recycling (Yellow)
  - 🟢 Garden Organics (Green)

## 🐳 Docker Deployment (Recommended)

**Important:** MQTT authentication is required for security. See [Home Assistant MQTT Setup](docs/HOMEASSISTANT_MQTT_SETUP.md) for complete setup instructions.

The easiest way to run this is with Docker:

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit with your details
nano .env

# 3. Start the container
docker-compose up -d
```

The container will automatically update your Home Assistant sensors every hour. See [DOCKER.md](DOCKER.md) for full documentation.

---

## 📋 Requirements

- **Docker** and Docker Compose
- **Home Assistant** with MQTT broker
- **Mushroom Cards** (via HACS)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/andrewkriley/ryde-waste-collection.git
cd ryde-waste-collection
```

### 2. Set Up MQTT in Home Assistant

Follow the complete guide: [Home Assistant MQTT Setup](docs/HOMEASSISTANT_MQTT_SETUP.md)

Quick steps:
1. Install Mosquitto broker add-on
2. Configure MQTT username/password
3. Add MQTT integration
4. Verify connection

### 3. Configure Container

Edit `.env`:

```bash
cp .env.example .env
nano .env
```

Required settings:
```env
RYDE_ADDRESS="Your Street Address, Ryde"
MQTT_BROKER="homeassistant.local"
MQTT_USER="ryde_waste"
MQTT_PASSWORD="your_secure_password"
```

### 4. Start Container

```bash
docker-compose up -d
```

Check logs:
```bash
docker-compose logs -f
```

You should see:
```
✓ Connected to MQTT broker
✓ Published General Waste: Wed 21/1/2026 (in 4 days)
✓ Published Recycling: Wed 21/1/2026 (in 4 days)
✓ Published Garden Organics: Wed 28/1/2026 (in 11 days)
```

### 5. Verify Sensors

In Home Assistant:
- Go to **Settings** → **Devices & Services** → **MQTT**
- Look for **"Ryde Waste Collection"** device
- Three sensors should appear automatically

### 6. Add Dashboard

See [Dashboard Setup Guide](docs/DASHBOARD_SETUP.md) for complete instructions.

Quick steps:
1. Install Mushroom Cards (via HACS)
2. Edit dashboard → Add Card → Manual
3. Copy contents of `homeassistant_mushroom_card.yaml`
4. Paste → Save → Done!

## 📊 Home Assistant Sensors

Three sensors are auto-created via MQTT Discovery:
- `sensor.ryde_waste_general` - General Waste collection
- `sensor.ryde_waste_recycling` - Recycling collection
- `sensor.ryde_waste_garden` - Garden Organics collection

Each sensor includes:
- `date` - ISO formatted date (YYYY-MM-DD)
- `date_formatted` - Human readable (e.g., "Wed 21/1/2026")
- `days_until` - Days until collection
- `upcoming` - Boolean (true if within 7 days)
- `color` - Indicator color (red/yellow/green)
- `collection_type` - Type of waste
- `last_updated` - Last update timestamp

## 🔧 Configuration Options

All configuration via `.env` file:

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `RYDE_ADDRESS` | Your address in Ryde LGA | `"123 Main St, Ryde NSW 2112"` |
| `MQTT_BROKER` | MQTT broker hostname | `"homeassistant.local"` |
| `MQTT_USER` | MQTT username | `"ryde_waste"` |
| `MQTT_PASSWORD` | MQTT password | `"secure_password"` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTT_PORT` | `1883` | MQTT broker port |
| `MQTT_TOPIC_PREFIX` | `ryde_waste` | Topic prefix for sensors |
| `UPDATE_INTERVAL` | `3600` | Update interval in seconds (1 hour) |
| `RUN_ON_STARTUP` | `true` | Run update on container start |
| `TZ` | `Australia/Sydney` | Timezone for logs |
| `DEBUG` | `false` | Enable debug mode |

## 📁 Project Structure

```
ryde-waste-collection/
├── ryde_waste_scraper.py           # Core scraper
├── ryde_mqtt_publisher.py          # MQTT publisher
├── Dockerfile                      # Docker image
├── docker-compose.yml              # Docker service
├── entrypoint.sh                   # Container entrypoint
├── requirements.txt                # Python dependencies
├── homeassistant_mushroom_card.yaml # Dashboard card
├── .env.example                    # Configuration template
├── .gitignore                      # Git ignore rules
├── .dockerignore                   # Docker ignore rules
├── LICENSE                         # MIT License
├── README.md                       # This file
├── CONTRIBUTING.md                 # Contribution guidelines
├── DOCKER.md                       # Docker deployment guide
├── MQTT.md                         # MQTT integration guide
└── docs/
    ├── HOMEASSISTANT_MQTT_SETUP.md # Complete MQTT setup
    ├── DASHBOARD_SETUP.md          # Dashboard creation
    ├── HOMEASSISTANT_SETUP.md      # HA configuration
    ├── VISUAL_EXAMPLE.md           # Dashboard examples
    ├── QUICK_START.md              # Quick reference
    └── PROJECT_STRUCTURE.md        # Project organization
```

## 🔧 Docker Commands

### Start
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Restart
```bash
docker-compose restart
```

### Stop
```bash
docker-compose down
```

### Rebuild after changes
```bash
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Sensors not appearing

1. Check container is running: `docker-compose ps`
2. View logs: `docker-compose logs -f`
3. Verify MQTT connection in logs
4. Check MQTT integration in Home Assistant
5. See [MQTT Setup Guide](docs/HOMEASSISTANT_MQTT_SETUP.md)

### Container keeps restarting

1. Check environment variables in `.env`
2. Verify MQTT credentials are correct
3. Ensure MQTT broker is running
4. Check logs for error messages

### Dashboard not showing data

1. Verify sensors exist: Developer Tools → States
2. Check Mushroom Cards are installed
3. Verify card YAML syntax
4. See [Dashboard Setup Guide](docs/DASHBOARD_SETUP.md)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an unofficial tool and is not affiliated with or endorsed by Ryde Council. Use responsibly and respect the council's website terms of service.

## 🙏 Acknowledgments

- Ryde Council for providing the waste collection service
- Home Assistant community
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) by piitaya

## 📚 Documentation

For detailed documentation, see:
- [Docker Deployment Guide](DOCKER.md)
- [MQTT Integration Guide](MQTT.md)
- [Home Assistant MQTT Setup](docs/HOMEASSISTANT_MQTT_SETUP.md)
- [Dashboard Setup Guide](docs/DASHBOARD_SETUP.md)
- [Visual Examples](docs/VISUAL_EXAMPLE.md)

---

**Made with ❤️ for the Ryde community**

**Docker + MQTT = Simple & Reliable** 🐳📡
