import db

def add_list(name, giftlist_type, user_id, password_hash):
    sql = "INSERT INTO giftlists (title, type, user_id, password_hash) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, giftlist_type, user_id, password_hash])

def get_lists():
    sql = "SELECT G.id id, G.title title, U.username username FROM giftlists G, users U WHERE G.user_id = U.id ORDER BY id DESC"
    return db.query(sql)

def get_list(list_id):
    sql = """SELECT G.id giftlist_id,
                    G.title,
                    G.type,
                    G.password_hash,
                    U.id user_id,
                    U.username
             FROM   giftlists G,
                    users U
             WHERE  G.user_id = U.id AND
                    G.id = ?
                    """
    result = db.query(sql, [list_id])
    return result[0] if result else None

def update_list(list_id, name, giftlist_type):
    sql = "UPDATE giftlists SET title = ?, type = ? WHERE id = ?"
    db.execute(sql, [name, giftlist_type, list_id])

def delete_list(list_id):
    sql = "DELETE FROM giftlists WHERE id = ?"
    db.execute(sql, [list_id])

def find(name, giftlist_type):
    if giftlist_type == "":
        sql = """SELECT G.id,
                        G.title,
                        G.type,
                        U.username
                FROM    giftlists G,
                        users U
                WHERE   G.title LIKE ? AND
                        G.user_id = U.id
                        """
        return db.query(sql, ["%" + name + "%"])
    else:
        sql = """SELECT G.id,
                        G.title,
                        G.type,
                        U.username
                 FROM   giftlists G,
                        users U
                 WHERE  (G.title LIKE ? AND G.type = ?) AND
                        G.user_id = U.id
                        """
        return db.query(sql, ["%" + name + "%", giftlist_type])

def get_list_passwordhash(list_id):
    sql = "SELECT password_hash FROM giftlists WHERE id = ?"
    return db.query(sql, [list_id])