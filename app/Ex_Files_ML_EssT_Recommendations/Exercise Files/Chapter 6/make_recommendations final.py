import numpy as np
import pandas as pd
import matrix_factorization_utilities

# Load user ratings
raw_dataset_df = pd.read_csv('movie_ratings_data_set.csv')

# Load movie titles
movies_df = pd.read_csv('movies.csv', index_col='movie_id')

# Convert the running list of user ratings into a matrix
ratings_df = pd.pivot_table(raw_dataset_df, index='user_id',
                            columns='movie_id',
                            aggfunc=np.max)

# Apply matrix factorization to find the latent features
U, M = matrix_factorization_utilities.low_rank_matrix_factorization(ratings_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=0.1)

# Find all predicted ratings by multiplying U and M matrices
predicted_ratings = np.matmul(U, M)

print("Enter a user_id to get recommendations (Between 1 and 100):")
user_id_to_search = int(input())

print("Movies previously reviewed by user_id {}:".format(user_id_to_search))

reviewed_movies_df = raw_dataset_df[raw_dataset_df['user_id'] == user_id_to_search]
reviewed_movies_df = reviewed_movies_df.join(movies_df, on='movie_id')

print(reviewed_movies_df[['title', 'genre', 'value']])

input("Press enter to continue.")

print("Movies we will recommend:")

user_ratings = predicted_ratings[user_id_to_search - 1]
movies_df['rating'] = user_ratings

already_reviewed = reviewed_movies_df['movie_id']
recommended_df = movies_df[movies_df.index.isin(already_reviewed) == False]
recommended_df = recommended_df.sort_values(by=['rating'], ascending=False)

print(recommended_df[['title', 'genre', 'rating']].head(5))

