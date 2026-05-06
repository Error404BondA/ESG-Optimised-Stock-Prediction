import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# 1. Enable tqdm to show a progress bar for pandas operations
tqdm.pandas()

# 2. Load your dataset
# Replace 'financial_news.csv' with your actual file path
print("Loading dataset...")
df = pd.read_csv('IndianFinancialNews.csv')

# 3. Initialize the FinBERT sentiment analysis pipeline
# We are using the ProsusAI/finbert model, an industry standard for this task.
# Note: Set device=0 if you have an NVIDIA GPU to speed this up, otherwise use device=-1 for CPU.
print("Downloading and loading FinBERT model...")
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=-1)

# 4. Define the scoring logic
def get_market_movement_score(text):
    try:
        # Run text through FinBERT. Truncation ensures it doesn't break on unusually long texts.
        result = sentiment_pipeline(str(text), truncation=True, max_length=512)[0]
        label = result['label']
        confidence = result['score']
        
        # Map the output to a directional continuous score (-1.0 to 1.0)
        # We multiply by confidence to give higher weight to strong, unambiguous signals
        if label == 'positive':
            return confidence        # e.g., +0.95
        elif label == 'negative':
            return -confidence       # e.g., -0.85
        else:
            return 0.0               # Neutral gets a flat 0
            
    except Exception as e:
        # Failsafe for empty rows or severe formatting issues
        return 0.0

# 5. Apply the model to your headlines
print(f"Processing {len(df)} headlines. This will take a few minutes...")
df['movement_score'] = df['headline'].progress_apply(get_market_movement_score)

# 6. Save the results back to a new CSV
output_filename = 'financial_news_scored.csv'
df.to_csv(output_filename, index=False)
print(f"Complete! Data saved to {output_filename}")