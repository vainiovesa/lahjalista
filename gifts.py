import db

def add_gift(title, giftlist_id):
    sql = "INSERT INTO gifts (title, giftlist_id) VALUES (?, ?)"
    db.execute(sql, [title, giftlist_id])

def get_gifts(giftlist_id):
    sql = """SELECT G.id,
                    G.title,
                    G.getter_id,
                    G.image IS NOT NULL has_image
             FROM   gifts G,
                    giftlists GL
             WHERE  GL.id = ? AND
                    G.giftlist_id = GL.id"""
    return db.query(sql, [giftlist_id])

def delete_gift(giftlist_id, gift_id):
    sql = "DELETE FROM gifts WHERE giftlist_id = ? AND id = ?"
    db.execute(sql, [giftlist_id, gift_id])

def buy(gift_id, buyer_id):
    sql = "UPDATE gifts SET getter_id = ? WHERE id = ?"
    db.execute(sql, [buyer_id, gift_id])

def cancel_buy(gift_id):
    sql = "UPDATE gifts SET getter_id = Null WHERE id = ?"
    db.execute(sql, [gift_id])

def get_list_id(gift_id):
    sql = "SELECT giftlist_id FROM Gifts WHERE id = ?"
    return db.query(sql, [gift_id])[0][0]

def get_buyer(gift_id):
    sql = "SELECT getter_id FROM Gifts WHERE id = ?"
    return db.query(sql, [gift_id])[0][0]

def users_buyings(username):
    sql = """SELECT G.title
             FROM   gifts G
             WHERE  getter_id = (SELECT id FROM users WHERE username = ?)"""
    return db.query(sql, [username])

def reserved(gift_id):
    sql = "SELECT getter_id FROM gifts WHERE id = ?"
    return db.query(sql, [gift_id])[0][0]

def get_gift(gift_id):
    sql = """SELECT G.id id,
                    G.title title,
                    G.giftlist_id giftlist_id,
                    GL.user_id user_id
             FROM   gifts G, giftlists GL 
             WHERE  G.id = ? AND
                    G.giftlist_id = GL.id"""
    result = db.query(sql, [gift_id])
    return result[0] if result else None

def update_image(gift_id, image):
    sql = "UPDATE gifts SET image = ? WHERE id = ?"
    db.execute(sql, [image, gift_id])

def get_image(gift_id):
    sql = "SELECT image FROM gifts WHERE id = ?"
    result = db.query(sql, [gift_id])
    return result[0][0] if result else None

def remove_image(gift_id):
    sql = "UPDATE gifts SET image = Null WHERE id = ?"
    db.execute(sql, [gift_id])