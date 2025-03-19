CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE giftlists (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type TEXT,
    user_id INTEGER REFERENCES users,
    password_hash TEXT
);