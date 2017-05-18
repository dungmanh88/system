import pickle
import pandas as pd
import numpy as np

# Load prediction rules from data files
M = pickle.load(open("product_features.dat", "rb"))

# Swap the rows and columns of product_features just so it's easier to work with
M = np.transpose(M)

# Load movie titles
movies_df = pd.read_csv('movies.csv', index_col='movie_id')

# Choose a movie to find similar movies to. Let's find movies similar to movie #5:
movie_id = 5

# Get movie #1's name and genre
movie_information = movies_df.loc[movie_id]

print("We are finding movies similar to this movie:")
print("Movie title: {}".format(movie_information.title))
print("Genre: {}".format(movie_information.genre))

# Get the features for movie #1 we found via matrix factorization
current_movie_features = M[movie_id - 1]

print("The attributes for this movie are:")
print(current_movie_features)

# The main logic for finding similar movies:

# 1. Subtract the current movie's features from every other movie's features
difference = M - current_movie_features

# 2. Take the absolute value of that difference (so all numbers are positive)
absolute_difference = np.abs(difference)

# 3. Each movie has several features. Sum those features to get a total 'difference score' for each movie
total_difference = np.sum(absolute_difference, axis=1)

# 4. Create a new column in the movie list with the difference score for each movie
movies_df['difference_score'] = total_difference

# 5. Sort the movie list by difference score, from least different to most different
sorted_movie_list = movies_df.sort_values('difference_score')

# 6. Print the result, showing the 5 most similar movies to movie_id #1
print("The five most similar movies are:")
print(sorted_movie_list[['title', 'difference_score']][0:5])
