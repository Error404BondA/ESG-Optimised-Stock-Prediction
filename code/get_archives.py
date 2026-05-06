import csv
import time
import random
from waybackpy import WaybackMachineCDXServerAPI

# Target URL and your "identity" for the archive
target_url = "https://www.business-standard.com/economy-policy"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_archive_data(start_year, end_year):
    # 1. Query the Archive for available snapshots in that range
    cdx = WaybackMachineCDXServerAPI(target_url, user_agent, start_timestamp=start_year, end_timestamp=end_year)
    
    # We'll save to CSV
    with open(f"bs_archive_{start_year}_{end_year}.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Archive_URL"])
        
        print(f"Finding snapshots between {start_year} and {end_year}...")
        
        # 2. Iterate through snapshots (Archive.org might have hundreds)
        # To avoid being slow, we'll pick one snapshot per month/week
        last_month = ""
        for item in cdx.snapshots():
            # item.timestamp is in format YYYYMMDDHHMMSS
            current_month = item.timestamp[:6] 
            
            if current_month != last_month:
                print(f"Found snapshot for {item.timestamp[:8]}")
                writer.writerow([item.timestamp, item.archive_url])
                last_month = current_month

    print("Step 1 Complete: Created a list of monthly snapshots.")

get_archive_data("2020", "2022")