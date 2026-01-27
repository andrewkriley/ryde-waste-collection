#!/usr/bin/env python3
"""
Ryde Council Waste Collection Scraper
Fetches waste collection information from Ryde Council using their public API.
"""

import requests
import re
import sys
import json
import argparse
from html import unescape


def search_address(address):
    """
    Search for an address and return the geolocation ID.
    
    Args:
        address (str): The address to search for
        
    Returns:
        dict: Dictionary containing id, address, ward, and score, or None if not found
    """
    url = "https://www.ryde.nsw.gov.au/api/v1/myarea/search"
    params = {"keywords": address}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("Items") and len(data["Items"]) > 0:
            # Return the first (highest scoring) result
            first_result = data["Items"][0]
            return {
                "id": first_result["Id"],
                "address": first_result["AddressSingleLine"],
                "ward": first_result.get("MunicipalSubdivision"),
                "score": first_result["Score"]
            }
    except requests.exceptions.RequestException as e:
        print(f"Error searching for address: {e}", file=sys.stderr)
    except (KeyError, ValueError) as e:
        print(f"Error parsing address search response: {e}", file=sys.stderr)
    
    return None


def get_waste_schedule(geolocation_id):
    """
    Get waste collection schedule for a geolocation ID.
    
    Args:
        geolocation_id (str): The geolocation ID from address search
        
    Returns:
        dict: Dictionary with waste types as keys and dates as values, or None if failed
    """
    url = "https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices"
    params = {
        "geolocationid": geolocation_id,
        "ocsvclang": "en-AU"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("success"):
            print("API returned success=false", file=sys.stderr)
            return None
        
        # Parse HTML content to extract waste collection dates
        html_content = unescape(data["responseContent"])
        
        schedule = {}
        
        # Extract General Waste date
        general_match = re.search(
            r'<h3>General Waste</h3>.*?<div class="next-service">\s*(.+?)\s*</div>',
            html_content,
            re.DOTALL
        )
        if general_match:
            schedule["General Waste"] = general_match.group(1).strip()
        
        # Extract Garden Organics date
        garden_match = re.search(
            r'<h3>Garden Organics</h3>.*?<div class="next-service">\s*(.+?)\s*</div>',
            html_content,
            re.DOTALL
        )
        if garden_match:
            schedule["Garden Organics"] = garden_match.group(1).strip()
        
        # Extract Recycling date
        recycling_match = re.search(
            r'<h3>Recycling</h3>.*?<div class="next-service">\s*(.+?)\s*</div>',
            html_content,
            re.DOTALL
        )
        if recycling_match:
            schedule["Recycling"] = recycling_match.group(1).strip()
        
        return schedule if schedule else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching waste schedule: {e}", file=sys.stderr)
    except (KeyError, ValueError) as e:
        print(f"Error parsing waste schedule response: {e}", file=sys.stderr)
    
    return None


def get_waste_collection_info(address):
    """
    Main function to get waste collection information for an address.
    
    Args:
        address (str): The address to look up
        
    Returns:
        dict: Dictionary with waste types as keys and dates as values, or None if failed
    """
    print(f"Searching for address: {address}")
    
    # Step 1: Search for the address
    address_result = search_address(address)
    
    if not address_result:
        print(f"Address not found: {address}", file=sys.stderr)
        return None
    
    print(f"Found: {address_result['address']}")
    print(f"Geolocation ID: {address_result['id']}")
    
    # Step 2: Get waste schedule
    print("Fetching waste collection schedule...")
    schedule = get_waste_schedule(address_result['id'])
    
    if not schedule:
        print("Failed to retrieve waste collection schedule", file=sys.stderr)
        return None
    
    return schedule


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Fetch waste collection information from Ryde Council"
    )
    parser.add_argument("address", help="The address to search for")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    
    args = parser.parse_args()
    
    # Get waste collection info
    waste_info = get_waste_collection_info(args.address)
    
    if waste_info:
        if args.json:
            print(json.dumps(waste_info, indent=2))
        else:
            print("\nWaste Collection Schedule:")
            print("-" * 40)
            for waste_type, date in waste_info.items():
                print(f"{waste_type:20s}: {date}")
        return 0
    else:
        print("\nFailed to retrieve waste collection information", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
