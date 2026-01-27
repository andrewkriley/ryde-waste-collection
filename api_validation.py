#!/usr/bin/env python3
"""
Ryde Council Waste Collection API Validation Script

This script validates the API-based approach for retrieving waste collection schedules.

APIs:
1. Address Search: https://www.ryde.nsw.gov.au/api/v1/myarea/search?keywords={address}
2. Waste Schedule: https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices?geolocationid={id}&ocsvclang=en-AU
"""

import requests
import json
import re
from html import unescape
from datetime import datetime


def search_address(address):
    """Search for an address and return the geolocation ID."""
    url = "https://www.ryde.nsw.gov.au/api/v1/myarea/search"
    params = {"keywords": address}
    
    response = requests.get(url, params=params)
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
    
    return None


def get_waste_schedule(geolocation_id):
    """Get waste collection schedule for a geolocation ID."""
    url = "https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices"
    params = {
        "geolocationid": geolocation_id,
        "ocsvclang": "en-AU"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data.get("success"):
        return None
    
    # Parse HTML content to extract waste collection dates
    html_content = unescape(data["responseContent"])
    
    schedule = {}
    
    # Extract General Waste date
    general_match = re.search(r'<h3>General Waste</h3>.*?<div class="next-service">\s*(.+?)\s*</div>', html_content, re.DOTALL)
    if general_match:
        schedule["general_waste"] = general_match.group(1).strip()
    
    # Extract Garden Organics date
    garden_match = re.search(r'<h3>Garden Organics</h3>.*?<div class="next-service">\s*(.+?)\s*</div>', html_content, re.DOTALL)
    if garden_match:
        schedule["garden_organics"] = garden_match.group(1).strip()
    
    # Extract Recycling date
    recycling_match = re.search(r'<h3>Recycling</h3>.*?<div class="next-service">\s*(.+?)\s*</div>', html_content, re.DOTALL)
    if recycling_match:
        schedule["recycling"] = recycling_match.group(1).strip()
    
    return schedule


def validate_address(address):
    """Validate a single address and print results."""
    print(f"\n{'='*60}")
    print(f"Testing: {address}")
    print(f"{'='*60}")
    
    # Step 1: Search for address
    print(f"\n1. Searching for address...")
    result = search_address(address)
    
    if not result:
        print(f"   ❌ Address not found")
        return False
    
    print(f"   ✓ Found: {result['address']}")
    print(f"   ✓ ID: {result['id']}")
    if result['ward']:
        print(f"   ✓ Ward: {result['ward']}")
    print(f"   ✓ Match Score: {result['score']:.2f}")
    
    # Step 2: Get waste schedule
    print(f"\n2. Fetching waste collection schedule...")
    schedule = get_waste_schedule(result['id'])
    
    if not schedule:
        print(f"   ❌ Failed to retrieve schedule")
        return False
    
    print(f"   ✓ General Waste: {schedule.get('general_waste', 'N/A')}")
    print(f"   ✓ Garden Organics: {schedule.get('garden_organics', 'N/A')}")
    print(f"   ✓ Recycling: {schedule.get('recycling', 'N/A')}")
    
    return True


def main():
    """Main validation function."""
    print("Ryde Council Waste Collection API Validation")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test address
    test_address = "129 Blaxland Road, Ryde"
    
    success = validate_address(test_address)
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    status = "✓ PASS" if success else "❌ FAIL"
    print(f"{status}: {test_address}")
    
    if success:
        print(f"\n✅ API validation passed!")
    else:
        print(f"\n⚠️  API validation failed. Review output above.")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
