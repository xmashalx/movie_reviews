import psycopg2
from dotenv import load_dotenv
import os


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def load_genres(genres: list[str]) -> dict:
    """Load genres into the database and return a mapping of genre names to IDs."""
    conn = get_connection()
    cur = conn.cursor()
    genre_name_to_id = {}

    for genre in genres:
        cur.execute("SELECT id FROM genre WHERE genre_name = %s", (genre,))
        result = cur.fetchone()
        if result:
            genre_name_to_id[genre] = result[0]
        else:
            cur.execute(
                "INSERT INTO genre (genre_name) VALUES (%s) RETURNING id",
                (genre,)
            )
            genre_name_to_id[genre] = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return genre_name_to_id


def load_directors(directors: list[str]) -> dict:
    """Load directors into the database and return a mapping of director names to IDs."""
    conn = get_connection()
    cur = conn.cursor()
    director_name_to_id = {}

    for director in directors:
        cur.execute(
            "SELECT id FROM director WHERE director_name = %s", (director,))
        result = cur.fetchone()
        if result:
            director_name_to_id[director] = result[0]
        else:
            cur.execute(
                """
                INSERT INTO director (director_name)
                VALUES (%s) RETURNING id
                """,
                (director,)
            )
            director_name_to_id[director] = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return director_name_to_id


def load_studios(studios: list[str]) -> dict:
    """Load studios into the database and return a mapping of studio names to IDs."""
    conn = get_connection()
    cur = conn.cursor()
    studio_name_to_id = {}

    for studio in studios:
        cur.execute("SELECT id FROM studio WHERE studio_name = %s", (studio,))
        result = cur.fetchone()
        if result:
            studio_name_to_id[studio] = result[0]
        else:
            cur.execute(
                """
                INSERT INTO studio (studio_name)
                VALUES (%s) RETURNING id
                """,
                (studio,)
            )
            studio_name_to_id[studio] = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return studio_name_to_id


def load_movies(movies: list[dict], director_name_to_id: dict, studio_name_to_id: dict) -> dict:
    """Load movies into the database but replace director and studio names with their IDs.
    returning a title movie id mapping."""
    conn = get_connection()
    cur = conn.cursor()

    title_to_id = {}

    for movie in movies:
        cur.execute("SELECT id FROM movie WHERE title = %s", (movie['title'],))
        result = cur.fetchone()
        if result:
            title_to_id[movie['title']] = result[0]
        else:
            director_id = director_name_to_id.get(movie['director_name'])
            studio_id = studio_name_to_id.get(movie['studio_name'])
            release_date = movie['release_date'] if movie['release_date'] else None

            cur.execute(
                """
                INSERT INTO movie (
                    title, release_date, score, overview,
                    studio_id, director_id, budget, revenue, cover_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """,
                (
                    movie['title'],
                    release_date,
                    movie['score'],
                    movie['overview'],
                    studio_id,
                    director_id,
                    movie['budget'],
                    movie['revenue'],
                    movie['cover_url']
                )
            )
            title_to_id[movie['title']] = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return title_to_id


def load_movie_genres(movie_genres: list[dict], title_to_id: dict, genre_name_to_id: dict):
    """Load movie-genre relationships into the database."""
    conn = get_connection()
    cur = conn.cursor()

    for mg in movie_genres:
        movie_id = title_to_id.get(mg['title'])
        genre_id = genre_name_to_id.get(mg['genre_name'])

        cur.execute(
            "SELECT 1 FROM movie_genres WHERE movie_id = %s AND genre_id = %s",
            (movie_id, genre_id)
        )
        if not cur.fetchone():
            cur.execute(
                """
                    INSERT INTO movie_genres (movie_id, genre_id)
                    VALUES (%s, %s)
                    """,
                (movie_id, genre_id)
            )

    conn.commit()
    cur.close()
    conn.close()
