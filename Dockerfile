FROM python:3.11-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    && wget -q -O /tmp/google-chrome-key.pub https://dl-ssl.google.com/linux/linux_signing_key.pub \
    && gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg /tmp/google-chrome-key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/google-chrome-key.pub

# Install matching ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}.0.6778.87/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip 2>/dev/null \
    || wget -q "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION}" -O /tmp/version.txt \
    && DRIVER_VERSION=$(cat /tmp/version.txt) \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip -q /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver* /tmp/version.txt

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

# Create directory for debug files
RUN mkdir -p /tmp/debug

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app /tmp/debug
USER appuser

# Health check - test MQTT connection
HEALTHCHECK --interval=1h --timeout=30s --start-period=10s --retries=3 \
    CMD python /app/ryde_mqtt_publisher.py "${RYDE_ADDRESS}" --mqtt-broker "${MQTT_BROKER}" --mqtt-port "${MQTT_PORT}" ${MQTT_USER:+--mqtt-user "${MQTT_USER}"} ${MQTT_PASSWORD:+--mqtt-password "${MQTT_PASSWORD}"} || exit 1

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
