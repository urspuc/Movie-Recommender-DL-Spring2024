import pandas as pd
import json

def load_keywords():
    df = pd.read_csv('data/keywords.csv')
    # Assuming 'keywords' column contains JSON-like strings
    df['keywords'] = df['keywords'].apply(lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else [])
    return df

def flatten_keywords(df):
    # This creates a list of keywords by exploding the parsed JSON
    df = df.explode('keywords')
    df['keyword_name'] = df['keywords'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
    return df.drop('keywords', axis=1)

def preprocess_keywords():
    keywords_df = load_keywords()
    keywords_df = flatten_keywords(keywords_df)
    # Further processing steps here
    return keywords_df

if __name__ == '__main__':
    keywords_processed = preprocess_keywords()
    keywords_processed.to_csv('data/processed_keywords.csv', index=False)
