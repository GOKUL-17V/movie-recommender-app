import streamlit as st
import pandas as pd
import numpy as np

# Load data
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")

# Merge datasets
movie_data = pd.merge(ratings, movies, on="movieId")

# Create a user-item matrix
user_movie_matrix = movie_data.pivot_table(index='userId', columns='title', values='rating')

# Function to get recommendations
def get_recommendations(movie_title, min_ratings=50):
    movie_ratings = user_movie_matrix[movie_title]
    similar_movies = user_movie_matrix.corrwith(movie_ratings)
    
    corr_df = pd.DataFrame(similar_movies, columns=["Correlation"])
    corr_df.dropna(inplace=True)
    
    rating_count = movie_data.groupby("title")["rating"].count()
    corr_df["count"] = rating_count
    
    recommendations = corr_df[corr_df["count"] >= min_ratings].sort_values("Correlation", ascending=False)
    return recommendations.head(10)

# Streamlit UI
st.title("🎬 Movie Recommender System")

movie_list = movies["title"].unique()
selected_movie = st.selectbox("Choose a movie:", sorted(movie_list))

if st.button("Get Recommendations"):
    try:
        recommendations = get_recommendations(selected_movie)
        st.write("Top 10 similar movies:")
        st.dataframe(recommendations)
    except:
        st.warning("Not enough data for this movie to recommend others.")
