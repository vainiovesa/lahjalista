import db

def add_gift(title, giftlist_id, getter_id=-1):
    sql = "INSERT INTO gifts (title, getter_id, giftlist_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, getter_id, giftlist_id])

def get_gifts(giftlist_id):
    sql = """SELECT G.title,
                    G.getter_id
            FROM    gifts G,
                    giftlists GL
            WHERE   GL.id = ? AND
                    G.giftlist_id = GL.id"""
    return db.query(sql, [giftlist_id])