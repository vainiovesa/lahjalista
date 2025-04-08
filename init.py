import os
import db

list_types = ["Hääjuhlan lahjatoivelista", "Syntymäpäiväjuhlan lahjatoivelista", "Valmistujaisten lahjatoivelista", "Muu lahjatoivelista"]

def create_tables():    
    if os.path.exists("database.db"):
        os.remove("database.db")
    db.execute("""CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password_hash TEXT
                );""")
    db.execute("""CREATE TABLE giftlists (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    user_id INTEGER REFERENCES users ON DELETE CASCADE,
                    password_hash TEXT
                );""")
    db.execute("""
                CREATE TABLE classes (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    value TEXT
                );""")
    for list_type in list_types:
        db.execute('INSERT INTO classes (title, value) VALUES ("type", ?)', [list_type])
    db.execute("""
                CREATE TABLE list_classes (
                    id INTEGER PRIMARY KEY,
                    list_id INTEGER REFERENCES giftlists ON DELETE CASCADE,
                    title TEXT,
                    value TEXT
                );""")
    db.execute("""
                CREATE TABLE gifts (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    getter_id INTEGER REFERENCES users,
                    giftlist_id INTEGER REFERENCES giftlists ON DELETE CASCADE
                );""")

if __name__=="__main__":
    create_tables()