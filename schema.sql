CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE giftlists (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    password_hash TEXT
);

CREATE TABLE gifts (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    getter_id INTEGER,
    giftlist_id INTEGER REFERENCES giftlists ON DELETE CASCADE
);
