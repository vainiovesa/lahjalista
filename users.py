import db

def add(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def find(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])