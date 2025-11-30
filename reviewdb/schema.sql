-- sql file to generate database
CREATE TABLE director (
    id INT GENERATED ALWAYS AS IDENTITY,
    director_name VARCHAR,
    PRIMARY KEY (id)
);
CREATE TABLE STUDIO (
    id INT GENERATED ALWAYS AS IDENTITY,
    STUDIO_NAME VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE users(
    id INT GENERATED ALWAYS AS IDENTITY,
    user_name VARCHAR,
    BIO VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE genre(
    id INT GENERATED ALWAYS AS IDENTITY,
    genre_name VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE movie(
    id INT GENERATED ALWAYS AS IDENTITY,
    title VARCHAR,
    release_date DATE,
    score FLOAT,
    overview VARCHAR,
    studio_id INT,
    director_id INT,
    budget FlOAT,
    revenue FLOAT,
    cover_url VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (studio_id) REFERENCES STUDIO(id),
    FOREIGN KEY (director_id) REFERENCES director(id)
);

CREATE TABLE movie_genres(
    id INT GENERATED ALWAYS AS IDENTITY,
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

CREATE TABLE review(
    id INT GENERATED ALWAYS AS IDENTITY,
    movie_id INT,
    user_id INT,
    rating INT,
    review_text VARCHAR,
    CREATED_AT DATE,
    PRIMARY KEY (id),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
\echo 'CREATED all tables: run the following command -> psql -d reviews -f insert.sql'