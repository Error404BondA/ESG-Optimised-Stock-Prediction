import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Load a specialized classification model
# Use device=0 for GPU, device=-1 for CPU
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

df = pd.read_csv("economic_times_headlines_2025.csv").head(200)
labels = ["Economy/Finance", "Other"]

results = []
# Process in batches of 32 for speed
for i in tqdm(range(0, len(df), 32)):
    batch = df['headline'].iloc[i:i+32].tolist()
    preds = classifier(batch, candidate_labels=labels)
    # Extract the top label for each headline
    batch_results = [p['labels'][0] for p in preds]
    results.extend(batch_results)

df['category'] = results
df[df['category'] == 'Economy/Finance'].to_csv("filtered_finance.csv", index=False)