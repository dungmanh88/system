import numpy as np
import pandas as pd
import matrix_factorization_utilities

# Load user ratings
raw_dataset_df = pd.read_csv('movie_ratings_data_set.csv')

# Convert the running list of user ratings into a matrix
ratings_df = pd.pivot_table(raw_dataset_df, index='user_id', columns='movie_id', aggfunc=np.max)

# Apply matrix factorization to find the latent features
U, M = matrix_factorization_utilities.low_rank_matrix_factorization(ratings_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=0.1)

# Find all predicted ratings by multiplying the U by M
predicted_ratings = np.matmul(U, M)

# Save all the ratings to a csv file
predicted_ratings_df = pd.DataFrame(index=ratings_df.index,
                                    columns=ratings_df.columns,
                                    data=predicted_ratings)
predicted_ratings_df.to_csv("predicted_ratings.csv")
