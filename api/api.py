"""Movies API"""
import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from datetime import datetime
from database import (
    get_db_connection, get_movies, get_movies_count,
    get_movie_by_id, get_reviews_for_movie, insert_review,
    get_all_users, get_user_by_id, get_reviews_by_user,
    add_user, verify_user_credentials,
    get_all_genres, get_all_directors, get_all_studios
)
from os import environ as ENV
from dotenv import load_dotenv
import os
from flask_caching import Cache

load_dotenv()
print("DB_HOST:", os.getenv("DATABASE_IP"))

print("DB_HOST:", os.getenv("DATABASE_IP"))
app = Flask(__name__)
app.secret_key = ENV.get("SECRET_KEY")
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})


@app.route('/')
def home():
    search = request.args.get('search', None)
    genre_id = request.args.get('genre_id', None)
    director_id = request.args.get('director_id', None)
    studio_id = request.args.get('studio_id', None)
    page = request.args.get('page', 1, type=int)
    per_page = 50

    conn = get_db_connection(ENV)

    movies = get_movies(conn, search, genre_id, director_id,
                        studio_id, page, per_page)
    total_movies = get_movies_count(
        conn, search, genre_id, director_id, studio_id)
    total_pages = (total_movies + per_page - 1) // per_page

    # Cache the dropdowns
    all_genres = cache.get('all_genres')
    if all_genres is None:
        all_genres = get_all_genres(conn)
        cache.set('all_genres', all_genres)

    all_directors = cache.get('all_directors')
    if all_directors is None:
        all_directors = get_all_directors(conn)
        cache.set('all_directors', all_directors)

    all_studios = cache.get('all_studios')
    if all_studios is None:
        all_studios = get_all_studios(conn)
        cache.set('all_studios', all_studios)

    conn.close()

    return render_template('home.html',
                           movies=movies,
                           all_genres=all_genres,
                           all_directors=all_directors,
                           all_studios=all_studios,
                           page=page,
                           total_pages=total_pages,
                           search=search,
                           genre_id=genre_id,
                           director_id=director_id,
                           studio_id=studio_id)


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
    if 'user_id' not in session:
        return redirect(url_for('login'))

    movie_id = int(id)
    user_id = session['user_id']
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')

    if not rating:
        flash('Please select a rating', 'error')
        return redirect(url_for('movie_detail', id=movie_id))

    if not review_text or review_text.strip() == '':
        flash('Please write a review', 'error')
        return redirect(url_for('movie_detail', id=movie_id))

    conn = get_db_connection(ENV)
    insert_review(conn, movie_id, user_id, int(rating), review_text)
    conn.close()

    flash('Review submitted successfully!', 'success')
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
