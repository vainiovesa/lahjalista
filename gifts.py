import db

def add_gift(title, giftlist_id):
    sql = "INSERT INTO gifts (title, giftlist_id) VALUES (?, ?)"
    db.execute(sql, [title, giftlist_id])

def get_gifts(giftlist_id):
    sql = """SELECT G.id,
                    G.title,
                    G.getter_id
             FROM   gifts G,
                    giftlists GL
             WHERE  GL.id = ? AND
                    G.giftlist_id = GL.id"""
    return db.query(sql, [giftlist_id])

def delete_gift(giftlist_id, gift_id):
    sql = "DELETE FROM gifts WHERE giftlist_id = ? AND id = ?"
    db.execute(sql, [giftlist_id, gift_id])

def buy(giftlist_id, gift_id, getter_id):
    sql = "UPDATE gifts SET getter_id = ? WHERE id = ? AND giftlist_id = ?"
    db.execute(sql, [getter_id, gift_id, giftlist_id])

def get_list_id_of_gift(gift_id):
    sql = "SELECT giftlist_id FROM Gifts WHERE id = ?"
    return db.query(sql, [gift_id])[0][0]

def users_buyings(username):
    sql = """SELECT G.title
             FROM   gifts G
             WHERE  getter_id = (SELECT id FROM users WHERE username = ?)"""
    return db.query(sql, [username])

def reserved(gift_id):
    sql = "SELECT getter_id FROM gifts WHERE id = ?"
    return db.query(sql, [gift_id])[0][0]