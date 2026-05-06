import pandas as pd
import requests
import io

def fetch_gkg_file(url):
    print(f"Fetching: {url}")
    r = requests.get(url)
    if r.status_code != 200:
        return None
    # pd.read_csv can handle ZIP files if you point it to the bytes
    return pd.read_csv(io.BytesIO(r.content), sep="\t", header=None, 
                       dtype=str, compression='zip', encoding='latin-1')

cols = [
    "GKGRECORDID","V2DATE","SourceCollectionIdentifier","SourceCommonName",
    "DocumentIdentifier","Counts","V2Counts","Themes","V2Themes","Locations",
    "V2Locations","Persons","V2Persons","Organizations","V2Organizations",
    "Tone","EnhancedDates","GCAM","SharingImage","RelatedImages","SocialImageEmbeds",
    "SocialVideoEmbeds","Quotations","AllNames","Amounts","TranslationInfo",
    "Extras"
]

all_news = []
limit = 5  # TEST LIMIT: Only download 5 files to see if it works
count = 0

# Test for January 2024
for day in range(1, 32):
    if count >= limit: break 
    
    date_str = f"202401{day:02d}"
    # Note: GDELT updates every 15 mins. 000000 is just the first slice of the day.
    url = f"http://data.gdeltproject.org/gdeltv2/{date_str}000000.gkg.csv.zip"
    
    try:
        df = fetch_gkg_file(url)
        if df is not None:
            df.columns = cols
            # Filter immediately to save memory
            filtered_df = df[df["DocumentIdentifier"].str.contains("thehindu.com", na=False)].copy()
            all_news.append(filtered_df)
            count += 1
    except Exception as e:
        print(f"Error on {date_str}: {e}")

if all_news:
    news_df = pd.concat(all_news, ignore_index=True)
    print(f"Success! Found {len(news_df)} articles.")
    news_df.to_csv("test_output.csv", index=False)
else:
    print("No data found. Check the URL or connection.")