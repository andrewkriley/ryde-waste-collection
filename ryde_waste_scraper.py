#!/usr/bin/env python3
"""
Ryde Council Waste Collection Schedule Scraper
Fetches waste collection dates for a given address
"""
import sys
import time
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

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
        try:
            address_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtAddressPublic-My-Area"))
            )
            print("Found address input field")
        except:
            print("ERROR: Could not find address input field")
            return None
        
        # Make sure the field is visible
        driver.execute_script("arguments[0].scrollIntoView(true);", address_input)
        time.sleep(1)
        
        # Clear and enter the address
        address_input.clear()
        address_input.send_keys(address)
        print("Address entered, waiting for autocomplete...")
        
        # Wait for Google Places autocomplete to appear
        time.sleep(3)
        
        # Try to select from autocomplete dropdown
        try:
            # Look for the pac-container (Google Places autocomplete dropdown)
            autocomplete_items = driver.find_elements(By.CSS_SELECTOR, ".pac-item")
            if autocomplete_items:
                print(f"Found {len(autocomplete_items)} autocomplete suggestions")
                # Click the first item
                autocomplete_items[0].click()
                print("Clicked first autocomplete suggestion")
            else:
                print("No autocomplete items found, pressing Enter")
                address_input.send_keys(Keys.RETURN)
        except:
            print("Fallback: pressing Enter")
            address_input.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        # Click the search button
        try:
            search_button = driver.find_element(By.NAME, "btnSearch_Public-My-Area")
            driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
            time.sleep(0.5)
            search_button.click()
            print("Clicked search button")
        except Exception as e:
            print(f"Could not click search button: {e}")
            # Try alternative - submit the form or press Enter
            try:
                address_input.send_keys(Keys.RETURN)
            except:
                pass
        
        # Wait for results to load
        print("Waiting for results...")
        time.sleep(8)
        
        if debug:
            with open('/tmp/ryde_result.html', 'w') as f:
                f.write(driver.page_source)
            print("Page source saved to /tmp/ryde_result.html")
        
        # Extract waste collection information
        page_source = driver.page_source
        
        # Look for waste collection data
        results = {}
        waste_types = ['General Waste', 'Garden Organics', 'Recycling']
        
        print("\nExtracting waste collection dates...")
        
        for waste_type in waste_types:
            # Search for the waste type and nearby date
            # Pattern allows for HTML tags between waste type and date
            pattern = re.compile(
                rf'{re.escape(waste_type)}.*?(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{{1,2}}/\d{{1,2}}/\d{{4}})',
                re.IGNORECASE | re.DOTALL
            )
            match = pattern.search(page_source)
            
            if match:
                day_of_week = match.group(1)
                date = match.group(2)
                full_date = f"{day_of_week} {date}"
                results[waste_type] = full_date
                print(f"  {waste_type}: {full_date}")
        
        if not results:
            print("\nNo waste collection dates found.")
            print("This could mean:")
            print("  - The address wasn't recognized")
            print("  - The page structure has changed")
            print("  - The address is outside the Ryde area")
            
            if not debug:
                print("\nRun with --debug flag to save page source for inspection")
            
            return None
        
        print(f"\nFound {len(results)}/{len(waste_types)} waste collection schedules")
        return results
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        driver.quit()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fetch waste collection dates from Ryde Council website'
    )
    parser.add_argument(
        'address',
        nargs='?',
        default='YOUR_ADDRESS',
        help='Address to search for (default: "YOUR_ADDRESS")'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Save page source for debugging'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Installing beautifulsoup4...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4', '--quiet'])
    
    results = get_waste_collection_info(args.address, debug=args.debug)
    
    if results:
        print("\n" + "="*60)
        print("WASTE COLLECTION SCHEDULE")
        print("="*60)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for waste_type, date in results.items():
                print(f"{waste_type}: {date}")
        
        print("="*60)
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
