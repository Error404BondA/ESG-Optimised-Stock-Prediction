import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

def scrape_moneycontrol_historical(start_year=2020, end_year=2024):
    # Moneycontrol's monthly sitemap URL pattern
    # Note: We use the mobile ('m.') subdomain as it often has fewer bot protections
    base_sitemap_url = "https://m.moneycontrol.com/news/sitemap/sitemap-post-{}-{:02d}.xml"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    historical_data = []
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13): # Months 1 through 12
            url = base_sitemap_url.format(year, month)
            print(f"Fetching data for {datetime(year, month, 1).strftime('%B %Y')}...")
            
            try:
                response = requests.get(url, headers=headers, timeout=15)
                
                # If the page exists, parse the XML
                if response.status_code == 200:
                    # We use 'xml' parser specifically for sitemaps
                    soup = BeautifulSoup(response.content, 'xml')
                    
                    # Find all <url> blocks in the sitemap
                    urls = soup.find_all('url')
                    
                    for loc_node in urls:
                        link_tag = loc_node.find('loc')
                        date_tag = loc_node.find('lastmod')
                        
                        if link_tag and date_tag:
                            link = link_tag.text
                            raw_date = date_tag.text
                            
                            # 1. Clean the Date 
                            # XML dates look like "2020-01-31T23:54:05+05:30"
                            try:
                                # Grab just the YYYY-MM-DD part before the 'T'
                                clean_date_str = raw_date.split('T')[0]
                                parsed_date = datetime.strptime(clean_date_str, "%Y-%m-%d")
                                # Format it to match your dataset: "January 31, 2020, Friday"
                                final_date = parsed_date.strftime("%B %d, %Y, %A")
                            except Exception:
                                final_date = "Unknown Date"
                                
                            # 2. Extract the Title from the URL
                            # URLs look like: ".../business/mcdonalds-profits-rise-9975571.html"
                            try:
                                # Get the last part of the URL, remove '.html', and drop the trailing ID numbers
                                slug = link.split('/')[-1].replace('.html', '')
                                # Split by '-' and drop the last item (which is usually the article ID)
                                words = slug.split('-')[:-1] 
                                # Join it back into a readable sentence
                                title = " ".join(words).capitalize()
                            except Exception:
                                title = link
                            
                            historical_data.append({
                                'Date': final_date,
                                'Title': title,
                                'URL': link
                            })
                else:
                    print(f"  -> Skipped (Status {response.status_code})")
                    
                # Be polite to the server
                time.sleep(1.5)
                
            except Exception as e:
                print(f"  -> Error fetching {year}-{month}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(historical_data)
    
    # Drop duplicates just in case
    df = df.drop_duplicates(subset=['Title'])
    return df

# --- Run the Historical Scraper ---
print("Initializing Historical Scraping Protocol...")
# Let's test it on just two months first (e.g., Jan-Feb 2020) to ensure it works
# Change to end_year=2024 when you are ready to do the massive pull!
df_historical = scrape_moneycontrol_historical(start_year=2020, end_year=2020) 

output_file = "moneycontrol_historical_2020.csv"
df_historical.to_csv(output_file, index=False)
print(f"\nMassive Success! Extracted {len(df_historical)} historical articles and saved to '{output_file}'")