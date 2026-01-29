"""Constants for the Ryde Waste Collection integration."""
from datetime import timedelta

DOMAIN = "ryde_waste_collection"

# Configuration
CONF_ADDRESS = "address"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_SCAN_INTERVAL = timedelta(hours=12)
DEFAULT_NAME = "Ryde Waste Collection"

# Waste types
WASTE_TYPE_GENERAL = "General Waste"
WASTE_TYPE_RECYCLING = "Recycling"
WASTE_TYPE_GARDEN = "Garden Organics"

WASTE_TYPES = [
    WASTE_TYPE_GENERAL,
    WASTE_TYPE_RECYCLING,
    WASTE_TYPE_GARDEN,
]

# Sensor mapping
SENSOR_TYPES = {
    WASTE_TYPE_GENERAL: {
        "key": "general_waste",
        "name": "General Waste",
        "icon": "mdi:trash-can",
    },
    WASTE_TYPE_RECYCLING: {
        "key": "recycling",
        "name": "Recycling",
        "icon": "mdi:recycle",
    },
    WASTE_TYPE_GARDEN: {
        "key": "garden_organics",
        "name": "Garden Organics",
        "icon": "mdi:leaf",
    },
}

# Attributes
ATTR_DAYS_UNTIL = "days_until"
ATTR_NEXT_COLLECTION = "next_collection"
ATTR_COLLECTION_DATE = "collection_date"
ATTR_ADDRESS = "address"
ATTR_GEOLOCATION_ID = "geolocation_id"
ATTR_LAST_UPDATED = "last_updated"

# API endpoints
API_SEARCH_URL = "https://www.ryde.nsw.gov.au/api/v1/myarea/search"
API_WASTE_URL = "https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices"
