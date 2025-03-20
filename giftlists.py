import db

def add_list(name, giftlist_type, user_id, password_hash):
    sql = "INSERT INTO giftlists (title, type, user_id, password_hash) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, giftlist_type, user_id, password_hash])

def get_lists():
    sql = "SELECT id, title FROM giftlists ORDER BY id DESC"
    return db.query(sql)

def get_list(list_id):
    sql = "SELECT G.title, G.type, U.username FROM giftlists G, users U WHERE G.user_id = U.id AND G.id = ?"
    return db.query(sql, [list_id])[0]
