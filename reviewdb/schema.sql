-- sql file to generate database
CREATE TABLE language(
    id INT GENERATED ALWAYS AS IDENTITY,
    language_name VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE country(
    id INT GENERATED ALWAYS AS IDENTITY,
    country_name VARCHAR,
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
    CREATED_AT DATE,
    UPDATED_AT DATE,
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
    language_id INT,
    budget FlOAT,
    revenue FLOAT,
    country_id INT,
    cover_url VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (studio_id) REFERENCES STUDIO(id),
    FOREIGN KEY (language_id) REFERENCES language(id),
    FOREIGN KEY (country_id) REFERENCES country(id)
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
    UPDATED_AT DATE,
    PRIMARY KEY (id),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
