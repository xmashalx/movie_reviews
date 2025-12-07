-- insert director
INSERT INTO director (director_name) VALUES ('Hayao Miyazaki'), ('Greta Gerwig'), ('Peter Weir');

-- insert studio
INSERT INTO STUDIO (STUDIO_NAME) VALUES ('Studio Ghibli'), ('A24'),('Touchstone Pictures');

-- insert movie
INSERT INTO movie (title, release_date, score, overview, studio_id, director_id, budget, revenue, cover_url)
VALUES (
  'Princess Mononoke',
  '1997-07-12',
  93.0,
  'The fate of the world rests on the courage of one warrior. Ashitaka, a prince of the disappearing Emishi people, is cursed by a demonized boar god and must journey to the west to find a cure. Along the way, he encounters San, a young human woman fighting to protect the forest, and Lady Eboshi, who is trying to destroy it. Ashitaka must find a way to bring balance to this conflict.',
  (SELECT id FROM STUDIO WHERE STUDIO_NAME = 'Studio Ghibli'),
  (SELECT id FROM director WHERE director_name = 'Hayao Miyazaki'),
  23500000,
  176506186,
  'https://m.media-amazon.com/images/M/MV5BZTcyN2Y0MDYtMGI1NC00MWQ1LWFhZGMtN2U4NTcxZGYyNjljXkEyXkFqcGc@._V1_.jpg'
), 
('Howls Moving Castle',
  '2004-11-20',
  88.0,
  'Sophie has an uneventful life at her late fathers hat shop, but all that changes when she befriends wizard Howl, who lives in a magical flying castle. However, the evil Witch of Waste takes issue and casts a spell on young sophie aging her prematurely. Now Howl must use all his magical talents to battle the witch and return sophie to her youth. ',
  (SELECT id FROM STUDIO WHERE STUDIO_NAME = 'Studio Ghibli'),
  (SELECT id FROM director WHERE director_name = 'Hayao Miyazaki'),
  24000000,
  236000000,
  'https://i.ebayimg.com/images/g/h9oAAOSw0BJgHam1/s-l1200.jpg'
),
(
  'Lady Bird',
  '2017-11-04',
  99.0,
  'A teenager navigates a loving but turbulent relationship with her strong willed mother over the course of an eventful and poignant senior year of high school.',
  (SELECT id FROM STUDIO WHERE STUDIO_NAME = 'A24'),
  (SELECT id FROM director WHERE director_name = 'Greta Gerwig'),
  10000000,
  78980000,
  'https://m.media-amazon.com/images/M/MV5BNjk5MzcyOWQtNzE1Mi00NzdmLTlkM2QtOTdjZThhMDc2Y2NjXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg'
),
(
  'Dead Poets Society',
  '1989-09-22',
  85.0,
  'A group of students in a highly conservative boarding school learn to rebel against the status quo and find deeper meaning in life with the help of their new poetry teacher.',
  (SELECT id FROM STUDIO WHERE STUDIO_NAME = 'Touchstone Pictures'),
  (SELECT id FROM director WHERE director_name = 'Peter Weir'),
  16400000,
  235900000,
  'https://resizing.flixster.com/DoSPDw8kGRPVM_1S1Y0GVUB9AYg=/fit-in/352x330/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/NowShowing/11995/11995_aa.jpg'
);

-- insert genre(s)
INSERT INTO genre (genre_name) VALUES ('Adventure'), ('Fantasy'), ('Anime'), ('Romance'), ('Comedy'), ('Drama');


-- link movie to genres
INSERT INTO movie_genres (movie_id, genre_id)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM genre WHERE genre_name = 'Adventure')
  ), (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM genre WHERE genre_name = 'Fantasy')
  ),  (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM genre WHERE genre_name = 'Anime')
  );


INSERT INTO movie_genres (movie_id, genre_id)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Howls Moving Castle'),
    (SELECT id FROM genre WHERE genre_name = 'Anime')
  ),
   (
    (SELECT id FROM movie WHERE title = 'Howls Moving Castle'),
    (SELECT id FROM genre WHERE genre_name = 'Fantasy')
  ), (
    (SELECT id FROM movie WHERE title = 'Howls Moving Castle'),
    (SELECT id FROM genre WHERE genre_name = 'Adventure')
  ), (
    (SELECT id FROM movie WHERE title = 'Howls Moving Castle'),
    (SELECT id FROM genre WHERE genre_name = 'Romance')
  );

INSERT INTO movie_genres (movie_id, genre_id) 
  VALUES (
    (SELECT id FROM movie WHERE title = 'Lady Bird'),
    (SELECT id FROM genre WHERE genre_name = 'Comedy')
  ),
   (
    (SELECT id FROM movie WHERE title = 'Lady Bird'),
    (SELECT id FROM genre WHERE genre_name = 'Drama')
  );

INSERT INTO movie_genres (movie_id, genre_id) 
  VALUES (
    (SELECT id FROM movie WHERE title = 'Dead Poets Society'),
    (SELECT id FROM genre WHERE genre_name = 'Comedy')
  ),
   (
    (SELECT id FROM movie WHERE title = 'Dead Poets Society'),
    (SELECT id FROM genre WHERE genre_name = 'Drama')
  );

-- insert user (you)
INSERT INTO users (user_name, BIO, password)
  VALUES ('Mashal', 'Lover of horror films.');

-- insert a review by you
INSERT INTO review (movie_id, user_id, rating, review_text, CREATED_AT)
  VALUES (
    (SELECT id FROM movie WHERE title = 'Princess Mononoke'),
    (SELECT id FROM users WHERE user_name = 'Mashal'),
    5,
    'A brutal but beautiful tale surrounding magical forests, severed limbs and the interaction between humans and our planet',
    CURRENT_DATE
  ),
  (
   (SELECT id FROM movie WHERE title = 'Howls Moving Castle'),
    (SELECT id FROM users WHERE user_name = 'Mashal'),
    5,
    'A film with a magical setting, a mix of weird charming and relatable characters, and a bizarre dream like storyline.',
    CURRENT_DATE
  ),
  (
    (SELECT id FROM movie WHERE title = 'Lady Bird'),
    (SELECT id FROM users WHERE user_name = 'Mashal'),
    5,
    'A great coming of age film and one of the few that portray the complexity of a mother daughter relationship.',
    CURRENT_DATE
  ),
  (
    (SELECT id FROM movie WHERE title = 'Dead Poets Society'),
    (SELECT id FROM users WHERE user_name = 'Mashal'),
    5,
    'Traumatising.',
    CURRENT_DATE
  );
