-- insert director
INSERT INTO director (director_name) VALUES ('Hayao Miyazaki');

-- insert studio
INSERT INTO STUDIO (STUDIO_NAME) VALUES ('Studio Ghibli');

-- insert movie
INSERT INTO movie (title, release_date, score, overview, studio_id, director_id, budget, revenue, cover_url)
VALUES (
  'Princess Mononoke',
  '1997-07-12',
  93.0,
  'The fate of the world rests on the courage of one warrior.
Ashitaka, a prince of the disappearing Emishi people, is cursed by a demonized boar god and must journey to the west to find a cure.
Along the way, he encounters San, a young human woman fighting to protect the forest, and Lady Eboshi, who is trying to destroy it. Ashitaka must find a way to bring balance to this conflict.',
  (SELECT id FROM STUDIO WHERE STUDIO_NAME = 'Studio Ghibli'),
  (SELECT id FROM director WHERE director_name = 'Hayao Miyazaki'),
  23500000,
  176506186,
  'https://m.media-amazon.com/images/M/MV5BZTcyN2Y0MDYtMGI1NC00MWQ1LWFhZGMtN2U4NTcxZGYyNjljXkEyXkFqcGc@._V1_.jpg'
);

-- insert genre(s)
INSERT INTO genre (genre_name) VALUES ('Adventure');
INSERT INTO genre (genre_name) VALUES ('Fantasy');
INSERT INTO genre (genre_name) VALUES ('Anime');

-- link movie to genres
INSERT INTO movie_genres (movie_id, genre_id)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM genre WHERE genre_name = 'Adventure')
  );
INSERT INTO movie_genres (movie_id, genre_id)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM genre WHERE genre_name = 'Fantasy')
  );
INSERT INTO movie_genres (movie_id, genre_id)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM genre WHERE genre_name = 'Anime')
  );

-- insert user (you)
INSERT INTO users (user_name, BIO, CREATED_AT, UPDATED_AT)
  VALUES ('mashal', 'lover of horror films', CURRENT_DATE, CURRENT_DATE);

-- insert a review by you
INSERT INTO review (movie_id, user_id, rating, review_text, CREATED_AT, UPDATED_AT)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM users WHERE user_name = 'mashal'),
    5,
    
'A brutal but beautiful tale surrounding magical forests, severed limbs and the interaction between humans and our planet',
    CURRENT_DATE,
    CURRENT_DATE
  );
