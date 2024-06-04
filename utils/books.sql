DROP TABLE IF EXISTS Books CASCADE;
DROP TABLE IF EXISTS Authors CASCADE;
DROP TABLE IF EXISTS Genre CASCADE;
DROP TABLE IF EXISTS written_by CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Reviews CASCADE;

CREATE TABLE IF NOT EXISTS Authors(
    author_id serial unique not null PRIMARY KEY,
    author_name text
);


CREATE TABLE IF NOT EXISTS Users(
    user_id serial unique not null PRIMARY KEY,
    user_name text
);

CREATE TABLE IF NOT EXISTS Genre(
    genre_id serial unique not null PRIMARY KEY,
    genre_name text
);

CREATE TABLE IF NOT EXISTS Books(
    ISBN serial unique not null PRIMARY KEY,
    -- author int not null REFERENCES Authors(author_id),
    -- genre int not null REFERENCES Genre(genre_id),
    title text,
    pages integer,
    avg_rating float,
    format varchar(100),
    descr text
);

CREATE TABLE IF NOT EXISTS written_by(
    author int not null REFERENCES Authors(author_id),
    book int not null REFERENCES Books(ISBN),
    PRIMARY KEY(author, book)
);

CREATE TABLE IF NOT EXISTS Reviews(
    review_id serial unique not null PRIMARY KEY,
    user_id int not null REFERENCES Users(user_id),
    book int not null REFERENCES Books(ISBN),
    review_text text,
    rating int
)
