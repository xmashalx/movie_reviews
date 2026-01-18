"""Implements the full ETl pipeline for movie data."""
import os
from dotenv import load_dotenv
import sys
from extract import (
    fetch_movie_genres,
    get_movie_ids_for_n_pages,
    get_full_movie_data_for_ids)
from transform import (
    transform_genres,
    transform_directors,
    transform_studios,
    transform_movies,
    transform_movie_genres)
from load import (
    load_genres,
    load_directors,
    load_studios,
    load_movies,
    load_movie_genres)


def main():
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    GENRES_API_URL = "https://api.themoviedb.org/3/genre/movie/list"
    MOVIE_DETAILS_API_URL = "https://api.themoviedb.org/3/movie"

    genres = fetch_movie_genres(GENRES_API_URL, API_KEY)

    # Check for --daily flag
    if len(sys.argv) > 1 and sys.argv[1] == "--daily":
        NOW_PLAYING_API_URL = "https://api.themoviedb.org/3/movie/now_playing"
        all_movie_ids = get_movie_ids_for_n_pages(
            NOW_PLAYING_API_URL, API_KEY, n_pages=2)
        print(
            f"Daily run: fetching {len(all_movie_ids)} now playing movies...")
    else:
        POPULAR_MOVIES_API_URL = "https://api.themoviedb.org/3/movie/popular"
        TOP_RATED_API_URL = "https://api.themoviedb.org/3/movie/top_rated"
        popular_ids = get_movie_ids_for_n_pages(
            POPULAR_MOVIES_API_URL, API_KEY, n_pages=15)
        top_rated_ids = get_movie_ids_for_n_pages(
            TOP_RATED_API_URL, API_KEY, n_pages=15)
        all_movie_ids = list(set(popular_ids + top_rated_ids))
        print(f"Full run: fetching {len(all_movie_ids)} unique movies...")

    full_movie_data = get_full_movie_data_for_ids(
        MOVIE_DETAILS_API_URL, all_movie_ids, API_KEY)
    print("Extraction complete.")

    # Transformation
    genre_names = transform_genres(genres)
    director_names = transform_directors(full_movie_data)
    studio_names = transform_studios(full_movie_data)
    transformed_movies = transform_movies(full_movie_data)
    movie_genres = transform_movie_genres(full_movie_data)
    print("Transformation complete.")

    # Load
    genre_name_to_id = load_genres(genre_names)
    director_name_to_id = load_directors(director_names)
    studio_name_to_id = load_studios(studio_names)
    title_to_id = load_movies(
        transformed_movies, director_name_to_id, studio_name_to_id)
    load_movie_genres(movie_genres, title_to_id, genre_name_to_id)
    print("Load complete.")


if __name__ == "__main__":
    main()
