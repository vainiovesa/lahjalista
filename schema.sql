CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE giftlists (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    password_hash TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE list_classes (
    list_id INTEGER PRIMARY KEY REFERENCES giftlists ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

CREATE TABLE gifts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    getter_id INTEGER REFERENCES users,
    giftlist_id INTEGER REFERENCES giftlists ON DELETE CASCADE,
    image BLOB
);

CREATE INDEX idx_gls_title_uid ON giftlists (title, user_id);
CREATE INDEX idx_gfs_glsid ON gifts (giftlist_id);