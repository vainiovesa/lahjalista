import db

def add_gift():
    pass

def get_gifts(giftlist_id):
    sql = """SELECT G.title,
                    G.getter_id
            FROM    gifts G,
                    giftlists GL
            WHERE   GL.id = ? AND
                    G.giftlist_id = GL.id"""
    return db.query(sql, [giftlist_id])