"""Movies API"""
import os
from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime
from database import (
    get_db_connection, get_movies, get_genres_for_movies,
    get_movie_by_id, get_reviews_for_movie, insert_review,
    get_all_users, get_user_by_id, get_reviews_by_user,
    add_user, verify_user_credentials,
    get_all_genres, get_all_directors, get_all_studios
)
from os import environ as ENV
from dotenv import load_dotenv

load_dotenv()
print("DB_HOST:", os.getenv("DATABASE_IP"))

app = Flask(__name__)
app.secret_key = ENV.get("SECRET_KEY")


@app.route('/')
def home():
    search = request.args.get('search', None)
    genre_id = request.args.get('genre_id', None)
    director_id = request.args.get('director_id', None)
    studio_id = request.args.get('studio_id', None)

    conn = get_db_connection(ENV)

    movies = get_movies(conn, search, genre_id,
                        director_id, studio_id)

    all_genres = get_all_genres(conn)
    all_directors = get_all_directors(conn)
    all_studios = get_all_studios(conn)

    conn.close()

    return render_template('home.html',
                           movies=movies,
                           all_genres=all_genres,
                           all_directors=all_directors,
                           all_studios=all_studios)


@app.route('/movie/<id>')
def movie_detail(id):
    movie_id = int(id)
    conn = get_db_connection(ENV)

    movie_information, genres = get_movie_by_id(conn, movie_id)
    reviews = get_reviews_for_movie(conn, movie_id)
    conn.close()
    return render_template('movie_detail.html',
                           movie=movie_information,
                           genres=genres,
                           reviews=reviews)


@app.route('/movie/<id>/review', methods=['POST'])
def post_review(id):
    if 'user_id' not in session:  # Check login first!
        return redirect(url_for('login'))
    movie_id = int(id)
    conn = get_db_connection(ENV)

    user_id = session['user_id']
    rating = int(request.form['rating'])
    review_text = request.form['review_text']

    insert_review(conn, movie_id, user_id, rating, review_text)
    conn.close()

    return redirect(url_for('movie_detail', id=movie_id))


@app.route('/users')
def users_list():
    conn = get_db_connection(ENV)
    users = get_all_users(conn)
    conn.close()
    return render_template('users.html',
                           users=users)


@app.route('/user/<id>')
def user_profile(id):
    user_id = int(id)
    conn = get_db_connection(ENV)
    user_info = get_user_by_id(conn, user_id)
    reviews = get_reviews_by_user(conn, user_id)
    conn.close()
    return render_template('user_profile.html',
                           user_info=user_info,
                           user_reviews=reviews)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        conn = get_db_connection(ENV)
        try:
            new_user = add_user(conn, username, bio, password)
            conn.close()
            session['user_id'] = new_user['id']
            return redirect(url_for('home'))
        except ValueError as e:
            conn.close()
            return render_template('register.html', error=e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection(ENV)
        user_id = verify_user_credentials(conn, username, password)
        conn.close()
        if not user_id:
            return render_template('login.html', error='error: username and password not found')
        session['user_id'] = user_id
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
