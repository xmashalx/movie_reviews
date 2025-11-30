"""Movies API"""

from flask import Flask, request
from datetime import datetime
from database import (get_db_connection, get_movies, get_movie_by_id,
                      create_movie, delete_movie, get_movie_by_country, get_movies_by_genre)


app = Flask(__name__)
conn = get_db_connection()
