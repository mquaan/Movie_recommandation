import streamlit as st
import pickle
import requests
import csv

st.title('Movie Recommender System')

# Reading the pickle data
with open("Data/movie_list.pkl", 'rb') as file:
    movies = pickle.load(file)

movie_list = movies['title'].values

with open("Data/similarity.pkl", 'rb') as file:
    similarity = pickle.load(file)

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=15d786cc910b647049be3fc40ce9f3a2&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    # Check if there are any matching rows
    matching_rows = movies[movies['title'] == movie]
    if not matching_rows.empty:
        movies_index = matching_rows.index[0]
        distances = similarity[movies_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        recommend_movies = []
        recommend_movie_posters = []

        for i in movies_list[1:6]:
            # Fetch poster from API
            movie_id = i[0]
            movie_id = movies.iloc[i[0]].id
            recommend_movie_posters.append(fetch_poster(movie_id))
            recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movie_posters

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
