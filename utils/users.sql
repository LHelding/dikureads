DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE IF NOT EXISTS Users(
    pk serial unique not null PRIMARY KEY,
	user_name varchar(50) UNIQUE,
    full_name varchar(50),
	password varchar(120)
);

INSERT INTO Users(user_name, full_name, password) VALUES ('admin', 'admin', 'admin');