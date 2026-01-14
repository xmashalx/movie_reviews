import requests
from dotenv import load_dotenv
import os
import time


def fetch_movie_genres(api_url, api_key):
    """Fetch movie genres from the developer API."""
    params = {"api_key": api_key}
    response = requests.get(api_url, params=params)
    print(response.json())
    return response.json()['genres']


def get_popular_movies(api_url, api_key, page=1):
    """Fetch popular movies from the developer API."""
    params = {"api_key": api_key, "page": page}
    response = requests.get(api_url, params=params)
    return response.json()


def get_movie_details(api_url, movie_id, api_key):
    """Fetch detailed information about a specific movie."""
    url = f"{api_url}/{movie_id}"
    params = {"api_key": api_key,
              "append_to_response": "credits,videos,images"}
    response = requests.get(url, params=params)
    return response.json()


def get_movie_ids_for_n_pages(api_url, api_key, n_pages):
    """Fetch movie IDs for n pages of popular movies."""
    movie_ids = []
    for page in range(1, n_pages + 1):
        popular_movies = get_popular_movies(api_url, api_key, page)
        for movie in popular_movies.get("results", []):
            movie_ids.append(movie["id"])
        time.sleep(0.25)  # to respect rate limits
    return movie_ids


def get_full_movie_data_for_ids(api_url, movie_ids, api_key):
    """Fetch full movie data for a list of movie IDs."""
    full_movie_data = []
    for movie_id in movie_ids:
        movie_data = get_movie_details(api_url, movie_id, api_key)
        full_movie_data.append(movie_data)
        time.sleep(0.25)  # to respect rate limits
    return full_movie_data


if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    GENRES_API_URL = "https://api.themoviedb.org/3/genre/movie/list"
    genres = fetch_movie_genres(GENRES_API_URL, API_KEY)
    print("Fetched Genres:", genres)
