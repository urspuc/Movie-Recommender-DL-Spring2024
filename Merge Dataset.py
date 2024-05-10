import pandas as pd

def load_data(file_name, usecols):
    df = pd.read_csv(file_name, header=0, sep='\t', quotechar='"', usecols=usecols)
    df.replace({'\\N': None}, inplace=True)  # Replace \N with None (NaN)
    return df

akas_columns = ['titleId', 'title']
basics_columns = ['tconst', 'titleType', 'isAdult', 'startYear', 'runtimeMinutes', 'genres']
crew_columns = ['tconst', 'directors']
ratings_columns = ['tconst', 'averageRating', 'numVotes']

PATH_RAW = "/Users/chenshengmai/Downloads"
# Load datasets with only required columns
title_akas = load_data( PATH_RAW + '/title.akas.tsv', akas_columns)
filtered_data = title_akas.groupby('titleId')

print("FINISHED 1")
title_basics = load_data(PATH_RAW + '/title.basics.tsv', basics_columns)
print("FINISHED 2")

title_crew = load_data(PATH_RAW + '/title.crew.tsv', crew_columns)
print("FINISHED 3")

title_ratings = load_data(PATH_RAW + '/title.ratings.tsv', ratings_columns)

# Merge datasets on 'tconst' and 'titleId'
merged_data = title_basics.merge(title_akas, left_on='tconst', right_on='titleId', how='left')
merged_data = merged_data.merge(title_crew, on='tconst', how='left')
merged_data = merged_data.merge(title_ratings, on='tconst', how='left')

# Convert data types
merged_data['isAdult'] = merged_data['isAdult'].astype(bool)
merged_data['startYear'] = pd.to_numeric(merged_data['startYear'], errors='coerce')
merged_data['runtimeMinutes'] = pd.to_numeric(merged_data['runtimeMinutes'], errors='coerce')
merged_data['averageRating'] = pd.to_numeric(merged_data['averageRating'], errors='coerce')
merged_data['numVotes'] = pd.to_numeric(merged_data['numVotes'], errors='coerce')

# Drop rows with any nulls in the columns we need to keep
merged_data.dropna(subset=['title', 'titleType', 'isAdult', 'startYear', 'runtimeMinutes', 'genres', 'directors', 'averageRating', 'numVotes'], inplace=True)

# Save or continue processing
merged_data.to_csv(PATH_RAW + '/processed_data.csv', index=False)


