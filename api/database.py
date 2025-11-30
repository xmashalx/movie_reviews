"""Script for functions that interact with database"""

from typing import Any
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from datetime import date
from psycopg2 import sql


def get_db_connection() -> connection:
    """Returns a live connection from the database."""
    conn = connect(dbname="moviesdb", cursor_factory=RealDictCursor)
    return conn


def get_movie_by_id(conn: connection, movie_id: int) -> dict[str, Any]:
    """Returns details of a single movie based on ID."""
    q = "SELECT * FROM movie WHERE id=%s;"
    with conn.cursor() as cur:
        cur.execute(q, (movie_id,))
        results = cur.fetchall()
    return results


def get_movies(conn: connection, search: str = None,
               sort_by: str = None, sort_order: str = None) -> list[dict]:
    """Returns details of all movies in database according to user search"""

    # setting up the query
    search = "%" + search + "%"
    q = sql.SQL(
        "SELECT * FROM movie WHERE title LIKE %s ORDER BY {} {}").format(sql.Identifier(sort_by), sql.SQL(sort_order))

    # execute teh query using cursor
    with conn.cursor() as cur:
        cur.execute(q, (search,))
        results = cur.fetchall()

    return results


def create_movie(conn: connection, title: str, release_date: date,
                 genre: str, overview: str, status: str, budget: int,
                 revenue: int, country: str, language: str, orig_title) -> dict:
    """post a new movies to the database"""
    q1 = """INSERT INTO movie 
    (title, release_date, score, overview, orig_title, movie_status, language_id, budget, revenue, country_id)
    VALUES (%s, %s, 0, %s, %s, %s, 
    (SELECT id from language WHERE language_name=%s), %s, %s, 
    (SELECT id FROM country WHERE country_name=%s)) RETURNING *;"""

    q2 = """INSERT INTO movie_genres
    (movie_id, genre_id) VALUES (%s, (SELECT id FROM genre WHERE genre_name=%s)) RETURNING *;"""

    with conn.cursor() as cur:
        cur.execute(q1, (title, release_date, overview,
                    orig_title, status, language, budget, revenue, country))
        results = cur.fetchall()
    with conn.cursor() as cur:
        cur.execute(q2, (results[0]["id"], genre))
        results2 = cur.fetchall()
    conn.commit()
    return results + results2


def delete_movie(conn: connection, movie_id: int) -> bool:
    """This executes a delete query to the database and returns true or false if deleted"""
    q = "DELETE FROM movie WHERE id=%s;"
    q2 = "DELETE FROM movie_genres WHERE movie_id=%s;"
    with conn.cursor() as cur:
        cur.execute(q2, (movie_id,))
        cur.execute(q, (movie_id,))
    conn.commit()
    return True


def get_movies_by_genre(conn: connection, genre_name: str, sort_by: str = None,
                        sort_order: str = None) -> list[dict[str, Any]]:
    """Return a list of movie data from a specific genre"""

    q = sql.SQL("""SELECT * FROM movie as m
               WHERE m.id IN (SELECT mg.movie_id FROM movie_genres as mg
                WHERE mg.genre_id =(SELECT g.id FROM genre as g WHERE genre_name=%s))
                ORDER BY {} {};""").format(sql.Identifier(sort_by), sql.SQL(sort_order))

    with conn.cursor() as cur:
        cur.execute(q, (genre_name, ))
        results = cur.fetchall()
    return results


def get_movie_by_country(conn: connection, country_code, sort_by: str = None,
                         sort_order: str = None) -> list[dict]:
    """Return a list of movie data from a specific country"""

    q = sql.SQL("""SELECT * FROM movie 
    WHERE country_id=(SELECT id FROM country WHERE country_name=%s)
    ORDER BY {} {};""").format(sql.Identifier(sort_by), sql.SQL(sort_order))

    with conn.cursor() as cur:
        cur.execute(q, (country_code,))
        results = cur.fetchall()
    return results
