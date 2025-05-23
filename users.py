import db

def add(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def find(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0] if result else None

def get_user(username):
    sql = "SELECT id, username FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0] if result else None

def get_lists(user_id):
    sql = "SELECT id, title FROM giftlists WHERE user_id = ? ORDER BY id DESC"
    result = db.query(sql, [user_id])
    return result if result else []