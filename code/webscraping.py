from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import urllib.parse

def scrape_historical_bs(query, start_date, end_date, filename="bs_archive_2020_2022.csv"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Constructing a Google search URL for specific site and dates
    # format: site:business-standard.com "economy" after:2020-01-01 before:2022-12-31
    search_query = f'site:business-standard.com "{query}" after:{start_date} before:{end_date}'
    url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

    try:
        print(f"Searching archives for {query} between {start_date} and {end_date}...")
        driver.get(url)
        time.sleep(5) # Wait for results to load

        # Google's search result blocks
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Only write header if file is new
            if file.tell() == 0:
                writer.writerow(["Headline", "Description", "Link"])

            count = 0
            for res in results:
                try:
                    headline = res.find_element(By.TAG_NAME, "h3").text
                    link = res.find_element(By.TAG_NAME, "a").get_attribute("href")
                    # Description is usually in the 'VwiC3b' class or similar
                    description = res.find_element(By.CSS_SELECTOR, "div[style*='-webkit-line-clamp']").text
                    
                    writer.writerow([headline, description, link])
                    count += 1
                except:
                    continue

        print(f"Successfully pulled {count} historical snippets into {filename}")
        
    finally:
        driver.quit()

# Execute for your specific range
scrape_historical_bs("economy", "2020-01-01", "2022-12-31")