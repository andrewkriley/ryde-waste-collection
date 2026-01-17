# Docker Deployment Guide

Run Ryde Waste Collection as a containerized application with automatic updates.

## 🚀 Quick Start

### 1. Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)

### 2. Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your details:

```bash
nano .env
```

Required values:
```env
RYDE_ADDRESS="Your Street Address, Ryde"
HA_URL="http://homeassistant.local:8123"
HA_TOKEN="your_long_lived_access_token"
```

### 3. Run with Docker Compose

```bash
docker-compose up -d
```

That's it! The container will:
- Run an initial update on startup
- Check for waste collection dates every hour (default)
- Automatically update your Home Assistant sensors
- Restart automatically if it crashes

## 📋 Configuration Options

All configuration is done via environment variables in the `.env` file:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `RYDE_ADDRESS` | Your address in Ryde LGA | `"123 Main St, Ryde NSW 2112"` |
| `HA_URL` | Home Assistant URL | `"http://192.168.1.100:8123"` |
| `HA_TOKEN` | HA Long-Lived Access Token | `"eyJ0eXAiOi..."` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `UPDATE_INTERVAL` | `3600` | Update interval in seconds (1 hour) |
| `RUN_ON_STARTUP` | `true` | Run update when container starts |
| `TZ` | `Australia/Sydney` | Timezone for logs |
| `DEBUG` | `false` | Enable debug mode (saves HTML) |

### Update Interval Examples

```env
UPDATE_INTERVAL=1800   # 30 minutes
UPDATE_INTERVAL=3600   # 1 hour (default)
UPDATE_INTERVAL=21600  # 6 hours
UPDATE_INTERVAL=86400  # 24 hours
```

**Recommendation:** Use 1-6 hours minimum to respect the council's website.

## 🔧 Docker Commands

### Start the container
```bash
docker-compose up -d
```

### Stop the container
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Restart the container
```bash
docker-compose restart
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

### Check container status
```bash
docker-compose ps
```

### Execute command in container
```bash
docker-compose exec ryde-waste-collection bash
```

## 📊 Monitoring

### View Live Logs
```bash
docker-compose logs -f ryde-waste-collection
```

### Check Health Status
```bash
docker inspect --format='{{.State.Health.Status}}' ryde-waste-collection
```

### View Last Update Time
Check the logs:
```bash
docker-compose logs --tail 20 ryde-waste-collection
```

## 🐛 Troubleshooting

### Container keeps restarting

Check logs:
```bash
docker-compose logs ryde-waste-collection
```

Common issues:
1. **Missing environment variables** - Verify `.env` file exists and is complete
2. **Invalid HA token** - Check token is valid and has correct permissions
3. **Network issues** - Ensure container can reach Home Assistant URL

### Enable Debug Mode

Edit `.env`:
```env
DEBUG=true
```

Restart container:
```bash
docker-compose restart
```

Debug files will be saved to `./debug/` directory.

### Test Configuration

Run a one-off test:
```bash
docker-compose run --rm ryde-waste-collection python /app/ryde_to_homeassistant.py \
  "$RYDE_ADDRESS" \
  --ha-url "$HA_URL" \
  --ha-token "$HA_TOKEN"
```

### View Container Resource Usage
```bash
docker stats ryde-waste-collection
```

## 🔐 Security

### Secrets Management

The container uses environment variables for configuration. For production:

1. **Never commit `.env` to git** (already in .gitignore)
2. **Use Docker secrets** for sensitive data (optional):

```yaml
secrets:
  ha_token:
    file: ./secrets/ha_token.txt
```

3. **Restrict file permissions**:
```bash
chmod 600 .env
```

### Network Security

The container needs to access:
- Ryde Council website (HTTPS)
- Your Home Assistant instance (HTTP/HTTPS)

Consider running Home Assistant with HTTPS if exposed beyond local network.

## 🎯 Advanced Usage

### Custom Docker Compose

Create `docker-compose.override.yml` for custom settings:

```yaml
version: '3.8'

services:
  ryde-waste-collection:
    # Custom network
    networks:
      - home-assistant
    
    # Different resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    
    # Custom volumes
    volumes:
      - ./custom-debug:/tmp/debug

networks:
  home-assistant:
    external: true
```

### Run on Different Schedule

Disable the built-in loop and use cron:

`.env`:
```env
RUN_ON_STARTUP=true
UPDATE_INTERVAL=999999  # Very long interval
```

Then use external cron or Home Assistant automations to trigger updates.

### Multiple Addresses

Run multiple containers for different addresses:

```yaml
services:
  ryde-waste-address-1:
    build: .
    env_file: .env.address1
    
  ryde-waste-address-2:
    build: .
    env_file: .env.address2
```

## 🏗️ Building from Source

### Build the image
```bash
docker build -t ryde-waste-collection .
```

### Run without compose
```bash
docker run -d \
  --name ryde-waste-collection \
  --restart unless-stopped \
  -e RYDE_ADDRESS="Your Address" \
  -e HA_URL="http://homeassistant.local:8123" \
  -e HA_TOKEN="your_token" \
  -e UPDATE_INTERVAL=3600 \
  ryde-waste-collection
```

## 📦 Pre-built Images

If pushing to Docker Hub:

```bash
docker pull username/ryde-waste-collection:latest
```

Update `docker-compose.yml`:
```yaml
services:
  ryde-waste-collection:
    image: username/ryde-waste-collection:latest
    # ... rest of config
```

## 🔄 Updates

### Update the container

Pull latest changes:
```bash
git pull
docker-compose up -d --build
```

### Update just the image
```bash
docker-compose pull
docker-compose up -d
```

## 📝 Environment Variables Reference

Complete list of all environment variables:

```env
# Required
RYDE_ADDRESS="Your Street Address, Ryde"
HA_URL="http://homeassistant.local:8123"
HA_TOKEN="your_long_lived_access_token"

# Optional - Scheduling
UPDATE_INTERVAL=3600        # Update interval in seconds
RUN_ON_STARTUP=true         # Run update on container start

# Optional - Localization
TZ=Australia/Sydney         # Timezone for logs

# Optional - Debugging
DEBUG=false                 # Enable debug mode
```

## 🎉 Success!

Your container is now running and will automatically:
- ✅ Update waste collection dates on schedule
- ✅ Publish to Home Assistant sensors
- ✅ Restart if it crashes
- ✅ Run updates on container restart

Check your Home Assistant dashboard for the Mushroom cards!

---

**Need help?** Check the [main README](README.md) or open an issue.
