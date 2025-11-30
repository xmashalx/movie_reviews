INSERT INTO language (language_name) VALUES ('English'),('French'),('Spanish'),('Japanese');
INSERT INTO COUNTRY (country_name) VALUES ('United Kingdom'), ('United States'), ('France'), ('Spain'), ('Japan');
INSERT INTO users (user_name, BIO, CREATED_AT, UPDATED_AT) VALUES ('mashal', 'Queen of the world: I LIKE MOVIES', CURRENT_DATE, CURRENT_DATE);
INSERT INTO genre (genre_name) VALUES ('Horror'), ('Comedy'),('Fantasy'),('Drama'),('Adventure'),('Thriller');
INSERT INTO STUDIO (STUDIO_NAME) VALUES ('STUDIO GHIBLI');
INSERT INTO movie
(title, release_date, score, overview, studio_id, language_id, budget, revenue, country_id, cover_url)
VALUES
('Princess Mononoke', '1997-07-12', 93,
'The fate of the world rests on the courage of one warrior.
Ashitaka, a prince of the disappearing Emishi people, is cursed by a demonized boar god and must journey to the west to find a cure.
Along the way, he encounters San, a young human woman fighting to protect the forest, and Lady Eboshi, who is trying to destroy it. Ashitaka must find a way to bring balance to this conflict.',
1, 1, 23500000, 169785704, 2, 'https://m.media-amazon.com/images/M/MV5BZTcyN2Y0MDYtMGI1NC00MWQ1LWFhZGMtN2U4NTcxZGYyNjljXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg');
INSERT INTO movie_genres (movie_id, genre_id) VALUES (1,3),(1,4),(1,5);
INSERT INTO review (movie_id, user_id, rating, review_text, CREATED_AT, UPDATED_AT)
VALUES
(1,1,10,
'A brutal but beautiful tale surrounding magical forests, severed limbs and the interaction between humans and our planet',
CURRENT_DATE, CURRENT_DATE)
