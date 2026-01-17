#!/usr/bin/env python3
"""
Ryde Waste Collection MQTT Publisher
Publishes waste collection dates to Home Assistant via MQTT Discovery
"""
import sys
import os
import json
import argparse
from datetime import datetime
import paho.mqtt.client as mqtt
import time

# Import the scraper function
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ryde_waste_scraper import get_waste_collection_info

def parse_date(date_string):
    """Parse date string like 'Wed 21/1/2026' to datetime object"""
    try:
        date_part = date_string.split(' ', 1)[1]
        return datetime.strptime(date_part, '%d/%m/%Y')
    except Exception as e:
        print(f"Error parsing date '{date_string}': {e}")
        return None

def days_until(date_obj):
    """Calculate days until the given date"""
    if not date_obj:
        return None
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    delta = date_obj - today
    return delta.days

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker"""
    if rc == 0:
        print("✓ Connected to MQTT broker")
    else:
        print(f"✗ Failed to connect to MQTT broker, return code {rc}")

def on_publish(client, userdata, mid):
    """Callback for when a message is published"""
    pass

def publish_mqtt_discovery(client, mqtt_topic_prefix, sensor_config):
    """
    Publish MQTT Discovery configuration for Home Assistant
    """
    entity_id = sensor_config['entity_id']
    discovery_topic = f"homeassistant/sensor/{entity_id}/config"
    
    discovery_payload = {
        "name": sensor_config['name'],
        "unique_id": entity_id,
        "state_topic": f"{mqtt_topic_prefix}/{entity_id}/state",
        "json_attributes_topic": f"{mqtt_topic_prefix}/{entity_id}/attributes",
        "icon": sensor_config['icon'],
        "device": {
            "identifiers": ["ryde_waste_collection"],
            "name": "Ryde Waste Collection",
            "model": "Waste Collection Monitor",
            "manufacturer": "Ryde Council Scraper"
        }
    }
    
    result = client.publish(discovery_topic, json.dumps(discovery_payload), retain=True)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"  ✓ Published discovery for {sensor_config['name']}")
    return result.rc == mqtt.MQTT_ERR_SUCCESS

def publish_sensor_data(client, mqtt_topic_prefix, entity_id, state, attributes):
    """
    Publish sensor state and attributes
    """
    state_topic = f"{mqtt_topic_prefix}/{entity_id}/state"
    attributes_topic = f"{mqtt_topic_prefix}/{entity_id}/attributes"
    
    # Publish state
    result1 = client.publish(state_topic, state, retain=True)
    
    # Publish attributes
    result2 = client.publish(attributes_topic, json.dumps(attributes), retain=True)
    
    return result1.rc == mqtt.MQTT_ERR_SUCCESS and result2.rc == mqtt.MQTT_ERR_SUCCESS

def publish_to_mqtt(waste_data, mqtt_broker, mqtt_port, mqtt_user, mqtt_password, mqtt_topic_prefix):
    """
    Publish waste collection data to MQTT with Home Assistant Discovery
    """
    # Mapping of waste types to sensor configs
    waste_config = {
        'General Waste': {
            'entity_id': 'ryde_waste_general',
            'name': 'General Waste Collection',
            'icon': 'mdi:trash-can',
            'color': 'red'
        },
        'Recycling': {
            'entity_id': 'ryde_waste_recycling',
            'name': 'Recycling Collection',
            'icon': 'mdi:recycle',
            'color': 'yellow'
        },
        'Garden Organics': {
            'entity_id': 'ryde_waste_garden',
            'name': 'Garden Organics Collection',
            'icon': 'mdi:leaf',
            'color': 'green'
        }
    }
    
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    # Set username and password if provided
    if mqtt_user and mqtt_password:
        client.username_pw_set(mqtt_user, mqtt_password)
    
    # Connect to broker
    try:
        print(f"Connecting to MQTT broker at {mqtt_broker}:{mqtt_port}...")
        client.connect(mqtt_broker, mqtt_port, 60)
        client.loop_start()
        time.sleep(1)  # Give it time to connect
    except Exception as e:
        print(f"✗ Failed to connect to MQTT broker: {e}")
        return False
    
    success_count = 0
    
    try:
        for waste_type, date_string in waste_data.items():
            if waste_type not in waste_config:
                continue
            
            config = waste_config[waste_type]
            date_obj = parse_date(date_string)
            days = days_until(date_obj)
            
            # Publish discovery configuration
            if publish_mqtt_discovery(client, mqtt_topic_prefix, config):
                # Prepare attributes
                attributes = {
                    'friendly_name': config['name'],
                    'icon': config['icon'],
                    'date': date_obj.strftime('%Y-%m-%d') if date_obj else None,
                    'date_formatted': date_string,
                    'days_until': days,
                    'collection_type': waste_type,
                    'color': config['color'],
                    'upcoming': days is not None and 0 <= days <= 7,
                    'last_updated': datetime.now().isoformat()
                }
                
                # Publish state and attributes
                if publish_sensor_data(client, mqtt_topic_prefix, config['entity_id'], date_string, attributes):
                    print(f"  ✓ Published {waste_type}: {date_string} (in {days} days)")
                    success_count += 1
                else:
                    print(f"  ✗ Failed to publish data for {waste_type}")
            else:
                print(f"  ✗ Failed to publish discovery for {waste_type}")
        
        time.sleep(1)  # Give messages time to be sent
        
    finally:
        client.loop_stop()
        client.disconnect()
    
    return success_count == len(waste_data)

def main():
    parser = argparse.ArgumentParser(
        description='Fetch waste collection dates and publish to MQTT'
    )
    parser.add_argument(
        'address',
        help='Address to search for'
    )
    parser.add_argument(
        '--mqtt-broker',
        required=True,
        help='MQTT broker hostname or IP'
    )
    parser.add_argument(
        '--mqtt-port',
        type=int,
        default=1883,
        help='MQTT broker port (default: 1883)'
    )
    parser.add_argument(
        '--mqtt-user',
        help='MQTT username (if required)'
    )
    parser.add_argument(
        '--mqtt-password',
        help='MQTT password (if required)'
    )
    parser.add_argument(
        '--mqtt-topic-prefix',
        default='ryde_waste',
        help='MQTT topic prefix (default: ryde_waste)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    print(f"Fetching waste collection dates for: {args.address}")
    print("=" * 60)
    
    # Fetch waste collection data
    waste_data = get_waste_collection_info(args.address, debug=args.debug)
    
    if not waste_data:
        print("✗ Failed to fetch waste collection data")
        return 1
    
    print("\nPublishing to MQTT...")
    print("=" * 60)
    
    # Publish to MQTT
    success = publish_to_mqtt(
        waste_data,
        args.mqtt_broker,
        args.mqtt_port,
        args.mqtt_user,
        args.mqtt_password,
        args.mqtt_topic_prefix
    )
    
    print("\n" + "=" * 60)
    if success:
        print("✓ Successfully published all sensors to MQTT")
        print("=" * 60)
        return 0
    else:
        print("✗ Failed to publish some sensors")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
