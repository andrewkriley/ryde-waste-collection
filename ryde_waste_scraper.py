#!/usr/bin/env python3
"""
Ryde Council Waste Collection Scraper
Fetches waste collection dates from the Ryde Council website
"""

import sys
import re
import time
import argparse
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_waste_collection_info(address, debug=False):
    """
    Fetch waste collection information for a given address from Ryde Council website
    
    Args:
        address: The address to search for
        debug: If True, save page source for debugging
    
    Returns:
        Dictionary with waste collection dates, or None if not found
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Detect if using Chrome or Chromium based on what's installed
    if os.path.exists('/usr/bin/google-chrome'):
        # amd64: Use Chrome with chromedriver
        chrome_options.binary_location = '/usr/bin/google-chrome'
        service = Service("/usr/local/bin/chromedriver")
    elif os.path.exists('/usr/bin/chromium'):
        # arm64: Use Chromium with chromium-driver
        chrome_options.binary_location = '/usr/bin/chromium'
        service = Service("/usr/bin/chromedriver")
    else:
        # Fallback: try default Chrome
        service = Service("/usr/local/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = 'https://www.ryde.nsw.gov.au/Information-Pages/My-area'
        print(f"Loading page: {url}")
        driver.get(url)
        
        # Wait for JavaScript to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Find the address input field
        print(f"Searching for address: {address}")
        address_input = driver.find_element(By.ID, "txtAddressPublic-My-Area")
        print("Found address input field")
        
        # Enter the address
        address_input.clear()
        address_input.send_keys(address)
        print("Address entered, waiting for autocomplete...")
        time.sleep(3)
        
        # Try to click on first autocomplete suggestion
        try:
            autocomplete_items = driver.find_elements(By.CSS_SELECTOR, ".pac-item")
            print(f"Found {len(autocomplete_items)} autocomplete suggestions")
            
            if autocomplete_items:
                autocomplete_items[0].click()
                print("Clicked first autocomplete suggestion")
                time.sleep(2)
            else:
                # No autocomplete suggestions, try pressing Enter
                print("No autocomplete items found, pressing Enter")
                address_input.send_keys(Keys.RETURN)
                time.sleep(2)
        except Exception as e:
            print(f"Could not interact with autocomplete: {e}")
            print("Attempting to click search button instead")
        
        # Try to click the search button
        try:
            search_button = driver.find_element(By.NAME, "btnSearch_Public-My-Area")
            search_button.click()
            print("Clicked search button")
        except Exception as e:
            print(f"Could not click search button: {e}")
        
        # Wait for results to load
        print("Waiting for results...")
        time.sleep(5)
        
        if debug:
            with open('/tmp/ryde_result.html', 'w') as f:
                f.write(driver.page_source)
            print("Page source saved to /tmp/ryde_result.html")
        
        # Get the page source and extract waste collection dates
        page_source = driver.page_source
        
        print("\nExtracting waste collection dates...")
        
        # Pattern to match dates in format like "Wed 21/1/2026"
        date_pattern = r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{1,2}/\d{1,2}/\d{4})'
        
        # Look for waste collection types and their dates
        waste_types = {
            'General Waste': None,
            'Garden Organics': None,
            'Recycling': None
        }
        
        for waste_type in waste_types.keys():
            # Find the waste type in the page
            type_pattern = re.compile(f'{waste_type}.*?{date_pattern}', re.IGNORECASE | re.DOTALL)
            match = type_pattern.search(page_source)
            
            if match:
                day = match.group(1)
                date = match.group(2)
                full_date = f"{day} {date}"
                waste_types[waste_type] = full_date
                print(f"  {waste_type}: {full_date}")
        
        # Check if we found all waste types
        found_count = sum(1 for v in waste_types.values() if v is not None)
        print(f"\nFound {found_count}/{len(waste_types)} waste collection schedules")
        
        if found_count > 0:
            return waste_types
        else:
            print("\n⚠️  Could not find waste collection dates")
            if not debug:
                print("Run with --debug flag to save page source for inspection")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        driver.quit()

def format_output(waste_data, json_format=False):
    """Format the waste collection data for display"""
    if json_format:
        import json
        return json.dumps(waste_data, indent=2)
    else:
        output = []
        for waste_type, date in waste_data.items():
            if date:
                output.append(f"{waste_type}: {date}")
            else:
                output.append(f"{waste_type}: Not found")
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Fetch waste collection dates from Ryde Council website'
    )
    parser.add_argument(
        'address',
        help='Address to search for (e.g., "54 North Road Ryde")'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Save page source for debugging'
    )
    
    args = parser.parse_args()
    
    print(f"Fetching waste collection dates for: {args.address}")
    print("=" * 60)
    
    results = get_waste_collection_info(args.address, debug=args.debug)
    
    if results:
        print("\n" + "=" * 60)
        print(format_output(results, args.json))
        print("=" * 60)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
