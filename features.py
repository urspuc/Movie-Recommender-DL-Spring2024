import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

class FeatureEngineer:
    """ 
    Director and Cast Extraction: Binary features for the presence of directors and top cast members.
    Keyword Features: Binary features for the presence of significant keywords.
    Textual Analysis: TF-IDF features derived from movie overviews.
    Integration: Combining all extracted features into a single DataFrame ready for use in modeling. 
    TODO:  dataframes (movies_df, credits_df, and keywords_df) need to be prepared as expected with the required preprocessing before using this class.
    """

    def __init__(self, movies_df, credits_df, keywords_df):
        self.movies = movies_df
        self.credits = credits_df
        self.keywords = keywords_df

    def extract_director_and_cast(self):
        # Extracting director names and top cast
        self.credits['director'] = self.credits['crew'].apply(lambda x: [d['name'] for d in x if d['job'] == 'Director'])
        self.credits['cast'] = self.credits['cast'].apply(lambda x: [c['name'] for c in x[:3]] if len(x) > 3 else [c['name'] for c in x])  # Top 3 cast
        mlb_director = MultiLabelBinarizer()
        mlb_cast = MultiLabelBinarizer()
        director_matrix = mlb_director.fit_transform(self.credits['director'])
        cast_matrix = mlb_cast.fit_transform(self.credits['cast'])
        return pd.DataFrame(director_matrix, columns=mlb_director.classes_), pd.DataFrame(cast_matrix, columns=mlb_cast.classes_)

    def keyword_features(self):
        # Extracting keyword features
        self.keywords['keyword_name'] = self.keywords['keywords'].apply(lambda x: [d['name'] for d in x])
        mlb_keywords = MultiLabelBinarizer()
        keyword_matrix = mlb_keywords.fit_transform(self.keywords['keyword_name'])
        return pd.DataFrame(keyword_matrix, columns=mlb_keywords.classes_)

    def process_text_data(self):
        # Textual features from movie overviews
        tfidf = TfidfVectorizer(max_features=100)
        overview_features = tfidf.fit_transform(self.movies['overview'].fillna(''))
        return pd.DataFrame(overview_features.toarray(), columns=tfidf.get_feature_names_out())

    def create_features(self):
        director_features, cast_features = self.extract_director_and_cast()
        keyword_features = self.keyword_features()
        text_features = self.process_text_data()
        # Merge features with the main movie DataFrame
        feature_df = pd.concat([self.movies, director_features, cast_features, keyword_features, text_features], axis=1)
        return feature_df

if __name__ == '__main__':
    # Assuming dataframes are loaded elsewhere and passed here
    fe = FeatureEngineer(movies_df, credits_df, keywords_df)
    featured_df = fe.create_features()
    featured_df.to_csv('data/featured_movies.csv', index=False)
