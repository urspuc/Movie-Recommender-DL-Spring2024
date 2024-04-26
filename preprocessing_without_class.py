import pandas as pd
import json


def load_data():
    # Load the CSV files
    movies = pd.read_csv('data/movies_metadata.csv', low_memory=False)
    ratings = pd.read_csv('data/ratings.csv')
    credits = pd.read_csv('data/credits.csv')
    keywords = pd.read_csv('data/keywords.csv')
    links = pd.read_csv('data/links.csv')
    links_small = pd.read_csv('data/links_small.csv')
    ratings_small = pd.read_csv('data/ratings_small.csv')

    return movies, ratings, credits, keywords, links, links_small, ratings_small




def safe_json_loads(x):  
    # Handle JSON decoding errors
    try:
        return json.loads(x.replace("'", "\"")) if isinstance(x, str) else {} # Replace single quotes with double quotes
    except json.JSONDecodeError as e:    
        with open('json_errors.log', 'a', encoding='utf-8') as f:
            f.write(f"Failed to decode JSON: {x}\n")
        return {}

def parse_json_columns(movies):
    # Parse JSON columns
    movies['genres'] = movies['genres'].apply(safe_json_loads)
    movies['production_companies'] = movies['production_companies'].apply(safe_json_loads)
    movies['production_countries'] = movies['production_countries'].apply(safe_json_loads)
    movies['spoken_languages'] = movies['spoken_languages'].apply(safe_json_loads)

    return movies


def clean_data(movies, ratings, credits, keywords, links, links_small, ratings_small):
    # Handle missing data
    movies = movies.dropna(subset=['title', 'genres']) 
    ratings = ratings.dropna(subset=['userId', 'movieId', 'rating'])    
    credits = credits.dropna(subset=['cast', 'crew'])
    keywords = keywords.dropna(subset=['id', 'keywords'])
    links = links.dropna(subset=['movieId', 'imdbId', 'tmdbId'])
    links_small = links_small.dropna(subset=['movieId', 'imdbId', 'tmdbId'])
    ratings_small = ratings_small.dropna(subset=['userId', 'movieId', 'rating'])
    movies.loc[:, 'runtime'].fillna(movies['runtime'].median()) # Replace missing runtime values with the median or mean

    # Convert data types
    ratings.loc[:, 'timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s') # Convert Unix timestamps to datetime
    ratings_small.loc[:, 'timestamp'] = pd.to_datetime(ratings_small['timestamp'], unit='s')
    movies.loc[:, 'budget'] = pd.to_numeric(movies['budget'], errors='coerce') # Convert budget and revenue to numeric
    movies.loc[:, 'revenue'] = pd.to_numeric(movies['revenue'], errors='coerce')
    movies.loc[:, 'popularity'] = pd.to_numeric(movies['popularity'], errors='coerce')
    movies.loc[:, 'vote_average'] = pd.to_numeric(movies['vote_average'], errors='coerce')
    movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce') # Convert strings to datetime
    movies = movies.dropna(subset=['release_date']) 

    # Extract year from release_date
    movies.loc[:, 'year'] = movies.loc[:, 'release_date'].dt.year

    # Drop unnecessary columns
    movies = movies.drop(columns=['imdb_id', 'homepage', 'original_title'])



    return movies, ratings, credits, keywords, links, links_small, ratings_small



def preprocess_data():
    movies, ratings, credits, keywords, links, links_small, ratings_small = load_data()
    movies, ratings, credits, keywords, links, links_small, ratings_small = clean_data(movies, ratings, credits, keywords, links, links_small, ratings_small)
    movies = parse_json_columns(movies)
    # Any additional preprocessing steps

    # Save preprocessed data to CSV files
    movies.to_csv('data/preprocessed_movies.csv', index=False)
    ratings.to_csv('data/preprocessed_ratings.csv', index=False)
    credits.to_csv('data/preprocessed_credits.csv', index=False)
    keywords.to_csv('data/preprocessed_keywords.csv', index=False)
    links.to_csv('data/preprocessed_links.csv', index=False)
    links_small.to_csv('data/preprocessed_links_small.csv', index=False)
    ratings_small.to_csv('data/preprocessed_ratings_small.csv', index=False)


if __name__ == '__main__':
    preprocess_data()


