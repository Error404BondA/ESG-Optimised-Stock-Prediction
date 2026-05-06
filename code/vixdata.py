import yfinance as yf
# INDIA VIX is the ticker for the Indian Volatility Index
vix_data = yf.download("^INDIAVIX", start="2006-01-01", end="2025-12-31")



# 2. Basic cleaning (Optional but recommended)
# This flattens the columns if yfinance returns them as a MultiIndex
vix_data.columns = [col[0] if isinstance(col, tuple) else col for col in vix_data.columns]

# 3. Save to CSV
vix_data.to_csv("india_vix_2020_2026.csv")

print("File saved successfully as 'india_vix_2020_2026.csv'")