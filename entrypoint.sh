#!/bin/bash
set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Ryde Waste Collection - Docker Container (MQTT)      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Validate required environment variables
if [ -z "$RYDE_ADDRESS" ]; then
    echo "❌ Error: RYDE_ADDRESS not set"
    exit 1
fi

if [ -z "$MQTT_BROKER" ]; then
    echo "❌ Error: MQTT_BROKER not set"
    exit 1
fi

# Enforce MQTT authentication for security
if [ -z "$MQTT_USER" ]; then
    echo "❌ Error: MQTT_USER not set"
    echo "   MQTT authentication is required for security"
    echo "   Please set MQTT_USER and MQTT_PASSWORD in your .env file"
    echo "   See docs/HOMEASSISTANT_MQTT_SETUP.md for setup instructions"
    exit 1
fi

if [ -z "$MQTT_PASSWORD" ]; then
    echo "❌ Error: MQTT_PASSWORD not set"
    echo "   MQTT authentication is required for security"
    echo "   Please set MQTT_USER and MQTT_PASSWORD in your .env file"
    echo "   See docs/HOMEASSISTANT_MQTT_SETUP.md for setup instructions"
    exit 1
fi

# Set defaults
MQTT_PORT=${MQTT_PORT:-1883}
MQTT_TOPIC_PREFIX=${MQTT_TOPIC_PREFIX:-ryde_waste}
UPDATE_INTERVAL=${UPDATE_INTERVAL:-3600}
RUN_ON_STARTUP=${RUN_ON_STARTUP:-true}
TZ=${TZ:-Australia/Sydney}

echo "📋 Configuration:"
echo "   Address: $RYDE_ADDRESS"
echo "   MQTT Broker: $MQTT_BROKER:$MQTT_PORT"
echo "   MQTT User: $MQTT_USER"
echo "   MQTT Authentication: ✓ Enabled"
echo "   MQTT Topic Prefix: $MQTT_TOPIC_PREFIX"
echo "   Update Interval: ${UPDATE_INTERVAL}s"
echo "   Timezone: $TZ"
echo ""

# Build MQTT command with required authentication
MQTT_CMD="python /app/ryde_mqtt_publisher.py \"$RYDE_ADDRESS\" \
    --mqtt-broker \"$MQTT_BROKER\" \
    --mqtt-port \"$MQTT_PORT\" \
    --mqtt-user \"$MQTT_USER\" \
    --mqtt-password \"$MQTT_PASSWORD\" \
    --mqtt-topic-prefix \"$MQTT_TOPIC_PREFIX\""

if [ "$DEBUG" = "true" ]; then
    MQTT_CMD="$MQTT_CMD --debug"
fi

# Function to run the update
run_update() {
    echo "⏰ $(date '+%Y-%m-%d %H:%M:%S') - Running update..."
    
    if eval $MQTT_CMD; then
        echo "✅ Update completed successfully"
    else
        echo "❌ Update failed"
        return 1
    fi
    
    echo ""
}

# Run on startup if enabled
if [ "$RUN_ON_STARTUP" = "true" ]; then
    echo "🚀 Running initial update on startup..."
    run_update
fi

# Main loop
echo "🔄 Starting update loop (interval: ${UPDATE_INTERVAL}s)"
echo "   Press Ctrl+C to stop"
echo ""

while true; do
    sleep "$UPDATE_INTERVAL"
    run_update
done
