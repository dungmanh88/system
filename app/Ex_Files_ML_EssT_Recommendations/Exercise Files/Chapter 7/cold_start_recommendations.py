import pickle
import pandas as pd

# Load prediction rules from data files
means = pickle.load(open("means.dat", "rb"))

# Load movie titles
movies_df = pd.read_csv('movies.csv', index_col='movie_id')

# Just use the average movie ratings directly as the user's predicted ratings
user_ratings = means

print("Movies we will recommend:")

movies_df['rating'] = user_ratings
movies_df = movies_df.sort_values(by=['rating'], ascending=False)

print(movies_df[['title', 'genre', 'rating']].head(5))