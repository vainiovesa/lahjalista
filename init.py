import os
import db

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
                    type TEXT,
                    user_id INTEGER REFERENCES users ON DELETE CASCADE,
                    password_hash TEXT
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