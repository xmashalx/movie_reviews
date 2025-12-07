"""Script for functions that interact with database"""

import bcrypt
from typing import Any
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from datetime import date
from psycopg2 import sql
from psycopg2 import Error
from os import environ as ENV, _Environ
from dotenv import load_dotenv  # Loads variables from a file into the environment

load_dotenv()


def get_db_connection(config: _Environ) -> connection:
    try:
        conn = connect(
            user=config.get("DATABASE_USERNAME"),
            # password=config.get("DATABASE_PASSWORD"),
            host=config.get("DATABASE_IP"),
            port=config.get("DATABASE_PORT"),
            database=config.get("DATABASE_NAME"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_movies(conn: connection, search: str = None, genre_id: int = None,
               director_id: int = None, studio_id: int = None) -> list[dict]:
    """get all movies in reviews and list them according to user search"""
    # setting up the query
    query = """
    SELECT m.*, d.director_name, s.studio_name 
    FROM movie AS m 
    JOIN director AS d ON m.director_id = d.id
    JOIN studio AS s ON m.studio_id = s.id
    """
    params = []
    conditions = []

    # Add conditions only if parameters are provided
    if search:
        conditions.append("m.title LIKE %s")
        params.append(f"%{search}%")

    if genre_id:
        conditions.append(
            "m.id IN (SELECT movie_id FROM movie_genres WHERE genre_id = %s)")
        params.append(genre_id)

    if director_id:
        conditions.append("m.director_id = %s")
        params.append(director_id)

    if studio_id:
        conditions.append("m.studio_id=%s")
        params.append(studio_id)

    # Combine everything
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Execute
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def get_genres_for_movies(conn: connection, movie_ids: list[int]) -> dict:
    """Get all genres for multiple movies"""

    placeholders = ','.join(['%s']*len(movie_ids))
    # Query to get genres for all these movie IDs
    query = f"""
        SELECT mg.movie_id, g.genre_name
        FROM movie_genres AS mg
        JOIN genre AS g ON mg.genre_id = g.id
        WHERE mg.movie_id IN ({placeholders});
    """

    # Execute query
    with conn.cursor() as cur:
        cur.execute(query, movie_ids)
        results = cur.fetchall()
    # Transform results into {movie_id: [genre1, genre2, ...]}
    genres_dict = {}
    for entry in results:
        if entry['movie_id'] in genres_dict:
            genres_dict[entry["movie_id"]].append(entry['genre_name'])
        else:
            genres_dict[entry["movie_id"]] = [entry["genre_name"]]

    return genres_dict


def get_movie_by_id(conn: connection, id: int) -> dict:
    """returns all info on a movie"""
    query_movie_info = """SELECT m.*, d.director_name, s.studio_name 
    FROM movie AS m
    JOIN director as d ON(m.director_id=d.id)
    JOIN studio as s ON(m.studio_id=s.id)
    WHERE m.id=%s;
    """
    query_movie_genres = """SELECT g.genre_name
        FROM movie_genres AS mg
        JOIN genre AS g ON mg.genre_id = g.id
        WHERE mg.movie_id=%s;"""

    with conn.cursor() as cur:
        cur.execute(query_movie_info, (id,))
        movie_info = cur.fetchone()  # or fetchall()?

        cur.execute(query_movie_genres, (id,))
        genres_info = cur.fetchall()

    return movie_info, genres_info


def get_reviews_for_movie(conn: connection, id: int) -> list[dict]:
    """get all the reviews for a movie and the user_name"""
    query = """SELECT r.*, u.user_name, m.title FROM review as r
    JOIN users as u ON(r.user_id=u.id)
    JOIN movie as m ON(r.movie_id=m.id)
    WHERE movie_id = %s;"""
    with conn.cursor() as cur:
        cur.execute(query, (id,))
        reviews_info = cur.fetchall()
    return reviews_info


def get_reviews_by_user(conn: connection, user_id: int) -> list[dict]:
    """get all the reviews for a single user"""
    query = """SELECT r.*, m.title
    FROM review as r
    JOIN movie as m ON(r.movie_id=m.id)
    WHERE user_id=%s;"""
    with conn.cursor() as cur:
        cur.execute(query, (user_id, ))
        result = cur.fetchall()
    return result


def insert_review(conn: connection, movie_id: int, user_id: int, rating: int, review_text: str) -> dict:
    """Function that will insert a review into the database"""
    if rating > 5 or rating < 1:
        raise ValueError("Rating must be an int between 1 and 5")
    query = """INSERT INTO review 
    (movie_id, user_id, rating, review_text, CREATED_AT)
    VALUES
    (%s, %s, %s, %s, CURRENT_DATE) RETURNING *;"""

    with conn.cursor() as cur:
        cur.execute(query, (movie_id, user_id, rating, review_text))
        results = cur.fetchone()
    conn.commit()
    return results


def get_all_genres(conn: connection) -> list[dict]:
    """return a list of all genres in the db"""
    query = """SELECT * FROM genre;"""
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    return results


def get_all_directors(conn: connection) -> list[dict]:
    """return a list of all directors in the db"""
    query = """SELECT * FROM director;"""
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    return results


def get_all_studios(conn: connection) -> list[dict]:
    """return a list of all studios in the db"""
    query = """SELECT * FROM studio;"""
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    return results


def get_all_users(conn: connection) -> list[dict]:
    """Return a list of all users"""
    query = """SELECT id, user_name, BIO FROM users ORDER BY user_name;"""
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    return results


def get_user_by_id(conn: connection, user_id: int) -> dict:
    """return a user profile from its id"""
    query = """SELECT id, user_name, BIO FROM users WHERE id=%s;"""
    with conn.cursor() as cur:
        cur.execute(query, (user_id,))
        results = cur.fetchone()
    return results


def add_user(conn: connection, username: str, bio: str, password: str) -> dict:
    """Register a new user with hashed password"""
    check_query = "SELECT id FROM users WHERE user_name = %s"
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Convert bytes to string for storage
    hashed_password_str = hashed_password.decode('utf-8')

    query = """INSERT INTO users (user_name, BIO, user_password) 
               VALUES (%s, %s, %s) RETURNING id, user_name, bio;"""

    with conn.cursor() as cur:
        cur.execute(check_query, (username,))
        if cur.fetchone():
            raise ValueError("Username already taken")
        cur.execute(query, (username, bio, hashed_password_str))
        results = cur.fetchone()
    conn.commit()
    return results


def verify_user_credentials(conn: connection, username, password) -> bool:
    query = """SELECT id, user_name, BIO, user_password FROM users WHERE user_name=%s;"""
    with conn.cursor() as cur:
        cur.execute(query, (username, ))
        results = cur.fetchone()
        if not results:
            return None
    stored_hash = results['user_password']
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return results['id']
    else:
        return None
