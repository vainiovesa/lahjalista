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
    id INTEGER PRIMARY KEY,
    list_id INTEGER REFERENCES giftlists ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

CREATE TABLE gifts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    getter_id INTEGER REFERENCES users,
    giftlist_id INTEGER REFERENCES giftlists ON DELETE CASCADE
);

INSERT INTO classes (title, value) VALUES ("type", "Hääjuhlan lahjatoivelista")
INSERT INTO classes (title, value) VALUES ("type", "Syntymäpäiväjuhlan lahjatoivelista")
INSERT INTO classes (title, value) VALUES ("type", "Valmistujaisten lahjatoivelista")
INSERT INTO classes (title, value) VALUES ("type", "Muu lahjatoivelista")