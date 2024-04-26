import pandas as pd
import json

def safe_parse_json(x):
    try:
        return json.loads(x.replace("'", "\"")) if isinstance(x, str) else []
    except json.JSONDecodeError as e:
        with open('json_parsing_errors.log', 'a', encoding='utf-8') as f:
            f.write(f"Error parsing JSON: {x} - Error: {e}\n")
        return []  # Return an empty list or another appropriate default value if JSON is corrupt


class KeywordPreprocessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_keywords(self):
        # Load the CSV file 
        df = pd.read_csv(f'{self.filepath}/keywords.csv')
        df['keywords'] = df['keywords'].apply(safe_parse_json)
        return df

    def flatten_keywords(self, df):
        # Explode the parsed JSON into separate rows
        df = df.explode('keywords')
        df['keyword_name'] = df['keywords'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
        return df.drop('keywords', axis=1)

    def preprocess_keywords(self):
        keywords_df = self.load_keywords()
        keywords_df = self.flatten_keywords(keywords_df)
        return keywords_df

if __name__ == '__main__':
    preprocessor = KeywordPreprocessor('data')
    keywords_processed = preprocessor.preprocess_keywords()
    keywords_processed.to_csv('data/processed_keywords.csv', index=False)
