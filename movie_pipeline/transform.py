""" This module contains transformation functions for movie data processing. """


def transform_genres(genre_data: list[dict]) -> list:
    """Transform raw genre data into a list of genre names."""
    return [genre['name'] for genre in genre_data]


def transform_directors(movie_data: list[dict]) -> list:
    """Transform raw movie data to extract directors into a DataFrame."""
    directors = []
    for movie in movie_data:
        for crew in movie.get('credits', {}).get('crew', []):
            if crew['job'] == 'Director':
                directors.append(crew['name'])
    return list(set(directors))


def transform_studios(movie_data: list[dict]) -> list:
    """Transform raw movie data to extract studios."""
    studios = []
    for movie in movie_data:
        companies = movie.get('production_companies', [])
        if companies:
            studios.append(companies[0]['name'])
    return list(set(studios))


def transform_movies(movie_data: list[dict]) -> list[dict]:
    """Transform raw movie data into a list of movie dicts."""
    TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
    movies = []

    for movie in movie_data:
        # Get director
        director = None
        for crew in movie.get('credits', {}).get('crew', []):
            if crew['job'] == 'Director':
                director = crew['name']
                break

        # Get primary studio
        companies = movie.get('production_companies', [])
        studio = companies[0]['name'] if companies else None

        # Build cover URL
        poster_path = movie.get('poster_path')
        cover_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else None

        transformed = {
            'title': movie.get('title'),
            'release_date': movie.get('release_date'),
            'score': movie.get('vote_average'),
            'overview': movie.get('overview'),
            'budget': movie.get('budget'),
            'revenue': movie.get('revenue'),
            'cover_url': cover_url,
            'director_name': director,
            'studio_name': studio,
        }
        movies.append(transformed)

    return movies


def transform_movie_genres(movie_data: list[dict]) -> list[dict]:
    """Transform raw movie data into a DataFrame of movie-genre relationships."""
    movie_genres = []

    for movie in movie_data:
        title = movie.get('title')
        genres = movie.get('genres', [])
        for genre in genres:
            movie_genres.append({
                'title': title,
                'genre_name': genre['name']
            })

    return movie_genres
