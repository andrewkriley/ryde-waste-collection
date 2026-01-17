# Home Assistant MQTT Setup Guide

Complete guide to setting up MQTT in Home Assistant for the Ryde Waste Collection integration.

## Prerequisites

- Home Assistant installed and running
- Access to Home Assistant configuration
- Admin access to create users

## Step-by-Step Setup

### Step 1: Install MQTT Broker

Home Assistant includes a built-in MQTT broker (Mosquitto) that's easy to set up.

#### Option A: Install Mosquitto Broker Add-on (Recommended)

1. Open Home Assistant
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Search for **"Mosquitto broker"**
4. Click **Install**
5. Wait for installation to complete
6. **IMPORTANT:** Go to the **Configuration** tab
7. Add a username and password:
   ```yaml
   logins:
     - username: ryde_waste
       password: your_secure_password_here
   ```
8. Click **Save**
9. Go to the **Info** tab
10. Click **Start**
11. Enable **Start on boot**
12. Enable **Watchdog**

#### Option B: Use External MQTT Broker

If you already have an external MQTT broker (like Mosquitto on another server):
- Skip to Step 2
- Use your broker's hostname/IP and credentials

### Step 2: Add MQTT Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **MQTT**
4. Click **MQTT**

Configure the integration:
- **Broker**: `localhost` (if using add-on) or your broker IP
- **Port**: `1883` (default)
- **Username**: `ryde_waste` (or your MQTT username)
- **Password**: Your secure password
- Click **Submit**

### Step 3: Verify MQTT is Working

1. Go to **Settings** → **Devices & Services** → **MQTT**
2. Click **Configure**
3. You should see:
   - **Connection Status**: Connected ✓
   - **Discovery**: Enabled ✓

### Step 4: Enable MQTT Discovery

MQTT Discovery should be enabled by default. Verify in `configuration.yaml`:

```yaml
mqtt:
  discovery: true
  discovery_prefix: homeassistant
```

If you need to add this:
1. Edit `/config/configuration.yaml`
2. Add the above configuration
3. Go to **Developer Tools** → **YAML** → **Check Configuration**
4. Click **Restart** → **Restart Home Assistant**

### Step 5: Create MQTT User (Optional but Recommended)

For better security, create a dedicated Home Assistant user for MQTT:

1. Go to **Settings** → **People**
2. Click **Add Person**
3. Fill in:
   - **Name**: MQTT Service
   - **Username**: `mqtt_service`
   - **Password**: Generate a strong password
   - **Can only login from local network**: ✓
   - **Administrator**: ✗ (not required)
4. Click **Create**

**Save these credentials** - you'll need them for the container configuration.

### Step 6: Test MQTT Connection

#### From Home Assistant

1. Go to **Developer Tools** → **MQTT**
2. In **Listen to a topic**, enter: `#` (listens to all topics)
3. Click **Start Listening**
4. In a new tab, go to **Publish a packet**
5. Topic: `test/message`
6. Payload: `Hello from Home Assistant`
7. Click **Publish**
8. You should see the message in the listening tab

#### From Command Line (Optional)

If you have `mosquitto-clients` installed:

```bash
# Subscribe to all topics
mosquitto_sub -h homeassistant.local -u ryde_waste -P your_password -t '#' -v

# Publish a test message (in another terminal)
mosquitto_pub -h homeassistant.local -u ryde_waste -P your_password -t 'test/topic' -m 'Hello'
```

### Step 7: Configure Container

Now configure the Ryde Waste Collection container with your MQTT credentials.

Edit `.env`:

```env
# Required
RYDE_ADDRESS="Your Street Address, Ryde"
MQTT_BROKER="homeassistant.local"  # or your HA IP address

# MQTT Authentication (REQUIRED for security)
MQTT_USER="ryde_waste"             # Username from Step 1
MQTT_PASSWORD="your_secure_password"  # Password from Step 1

# Optional
MQTT_PORT=1883
MQTT_TOPIC_PREFIX=ryde_waste
UPDATE_INTERVAL=3600
RUN_ON_STARTUP=true
TZ=Australia/Sydney
DEBUG=false
```

### Step 8: Start the Container

```bash
docker-compose up -d
```

### Step 9: Verify Sensors Appear

Within 1-2 minutes, check Home Assistant:

1. Go to **Settings** → **Devices & Services** → **MQTT**
2. Click on **MQTT** integration
3. Look for **"Ryde Waste Collection"** device
4. Click on it - you should see 3 sensors:
   - General Waste Collection
   - Recycling Collection  
   - Garden Organics Collection

Alternatively, go to **Developer Tools** → **States** and search for:
- `sensor.ryde_waste_general`
- `sensor.ryde_waste_recycling`
- `sensor.ryde_waste_garden`

### Step 10: Check Container Logs

Verify the container is working:

```bash
docker-compose logs -f ryde-waste-collection
```

You should see:
```
✓ Connected to MQTT broker
✓ Published discovery for General Waste Collection
✓ Published General Waste: Wed 21/1/2026 (in 4 days)
✓ Published discovery for Recycling Collection
...
```

## Troubleshooting

### Error: Connection Refused

**Cause**: MQTT broker not accessible

**Solutions**:
1. Verify Mosquitto add-on is running
2. Check broker hostname/IP is correct
3. Test connectivity: `ping homeassistant.local`
4. Try using IP address instead of hostname

### Error: Authentication Failed

**Cause**: Wrong username or password

**Solutions**:
1. Verify credentials in Mosquitto add-on configuration
2. Check `.env` file has correct username/password
3. Ensure no extra spaces in credentials
4. Try recreating the MQTT user in Mosquitto config

### Sensors Not Appearing

**Cause**: Various possible issues

**Solutions**:
1. Check MQTT Discovery is enabled:
   ```yaml
   mqtt:
     discovery: true
   ```
2. Restart Home Assistant: **Settings** → **System** → **Restart**
3. Check container logs: `docker-compose logs -f`
4. Verify topics in MQTT:
   - **Developer Tools** → **MQTT** → Listen to topic: `homeassistant/sensor/#`
5. Clear MQTT discovery cache:
   ```bash
   # Delete discovery messages and restart container
   docker-compose restart
   ```

### Error: Connection Timeout

**Cause**: Firewall or network issue

**Solutions**:
1. Check firewall allows port 1883
2. If using external broker, verify network connectivity
3. Try connecting from container to broker:
   ```bash
   docker-compose exec ryde-waste-collection ping homeassistant.local
   ```

### Sensors Show "Unavailable"

**Cause**: Container not updating MQTT topics

**Solutions**:
1. Check container is running: `docker-compose ps`
2. Restart container: `docker-compose restart`
3. Check logs for errors: `docker-compose logs -f`
4. Verify UPDATE_INTERVAL isn't too large

## Security Best Practices

### 1. Use Strong Passwords

Generate secure passwords:
```bash
# On Linux/Mac
openssl rand -base64 32

# Or use a password manager
```

### 2. Restrict MQTT User Permissions

In Mosquitto configuration, you can restrict topics:

```yaml
logins:
  - username: ryde_waste
    password: your_secure_password
    
acl:
  - username: ryde_waste
    topic: ryde_waste/#
    access: write
  - username: ryde_waste
    topic: homeassistant/sensor/#
    access: write
```

### 3. Use TLS/SSL (Advanced)

For encrypted MQTT connections:

1. Configure Mosquitto with certificates
2. Update container:
   ```env
   MQTT_PORT=8883
   MQTT_USE_TLS=true
   ```

### 4. Network Isolation

Run container on same Docker network as Home Assistant:

```yaml
# docker-compose.yml
networks:
  - homeassistant

networks:
  homeassistant:
    external: true
```

## Advanced Configuration

### Multiple MQTT Brokers

If you have multiple MQTT brokers, you can specify different ones:

```env
MQTT_BROKER=mqtt-primary.local
# Or use IP
MQTT_BROKER=192.168.1.50
```

### Custom Discovery Prefix

If your Home Assistant uses a custom discovery prefix:

```yaml
# configuration.yaml
mqtt:
  discovery_prefix: my_custom_prefix
```

Update the container code in `ryde_mqtt_publisher.py`:
```python
discovery_topic = f"my_custom_prefix/sensor/{entity_id}/config"
```

### MQTT Over WebSockets

If your broker uses WebSockets:

```env
MQTT_PORT=9001
MQTT_TRANSPORT=websockets
```

## Verification Checklist

Before starting the container, verify:

- [ ] Mosquitto broker add-on is installed and running
- [ ] MQTT integration is configured in Home Assistant
- [ ] MQTT username and password are set in Mosquitto config
- [ ] Discovery is enabled in MQTT configuration
- [ ] `.env` file has correct MQTT credentials
- [ ] Container can reach Home Assistant network
- [ ] Port 1883 is accessible

## Common MQTT Topics

The container publishes to these topics:

```
# Discovery topics (auto-register sensors)
homeassistant/sensor/ryde_waste_general/config
homeassistant/sensor/ryde_waste_recycling/config
homeassistant/sensor/ryde_waste_garden/config

# State topics (sensor values)
ryde_waste/ryde_waste_general/state
ryde_waste/ryde_waste_recycling/state
ryde_waste/ryde_waste_garden/state

# Attribute topics (sensor metadata)
ryde_waste/ryde_waste_general/attributes
ryde_waste/ryde_waste_recycling/attributes
ryde_waste/ryde_waste_garden/attributes
```

## Summary

Once configured:
1. ✅ MQTT broker running in Home Assistant
2. ✅ MQTT integration configured with authentication
3. ✅ Container configured with MQTT credentials
4. ✅ Sensors auto-discover and appear in Home Assistant
5. ✅ No manual automations needed!

---

**Need help?** Check the [MQTT.md](../MQTT.md) guide or [DOCKER.md](../DOCKER.md) for container-specific issues.
