FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ryde_waste_scraper.py .
COPY ryde_mqtt_publisher.py .
COPY entrypoint.sh .

# Make scripts executable
RUN chmod +x entrypoint.sh ryde_mqtt_publisher.py

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check - test MQTT connection
HEALTHCHECK --interval=1h --timeout=30s --start-period=10s --retries=3 \
    CMD python /app/ryde_mqtt_publisher.py "${RYDE_ADDRESS}" --mqtt-broker "${MQTT_BROKER}" --mqtt-port "${MQTT_PORT}" ${MQTT_USER:+--mqtt-user "${MQTT_USER}"} ${MQTT_PASSWORD:+--mqtt-password "${MQTT_PASSWORD}"} || exit 1

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
