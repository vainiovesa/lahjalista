import db

def add_list(name, classes:list, user_id, password_hash):
    sql_giftlist = "INSERT INTO giftlists (title, user_id, password_hash) VALUES (?, ?, ?)"
    sql_classes = "INSERT INTO list_classes (list_id, title, value) VALUES (?, ?, ?)"
    list_id = db.execute(sql_giftlist, [name, user_id, password_hash])
    for title, value in classes:
        db.execute(sql_classes, [list_id, title, value])

def get_lists(page_size, page):
    sql = """SELECT   G.id id, G.title title, U.username username 
             FROM     giftlists G, users U
             WHERE    G.user_id = U.id
             ORDER BY id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_list(list_id):
    sql = """SELECT G.id giftlist_id,
                    G.title,
                    G.password_hash,
                    U.id user_id,
                    U.username,
                    L.value type
             FROM   giftlists G,
                    users U,
                    list_classes L
             WHERE  G.user_id = U.id AND
                    G.id = L.list_id AND
                    G.id = ?
                    """
    result = db.query(sql, [list_id])
    return result[0] if result else None

def update_list(list_id, name, classes:list):
    sql_giftlist = "UPDATE giftlists SET title = ? WHERE id = ?"
    sql_classes = "UPDATE list_classes SET value = ? WHERE list_id = ? AND title = ?"
    db.execute(sql_giftlist, [name, list_id])
    for title, value in classes:
        db.execute(sql_classes, [value, list_id, title])

def delete_list(list_id):
    sql = "DELETE FROM giftlists WHERE id = ?"
    db.execute(sql, [list_id])

def find(name, giftlist_type):
    if giftlist_type == "":
        sql = """SELECT G.id,
                        G.title,
                        U.username,
                        L.value
                FROM    giftlists G,
                        users U,
                        list_classes L
                WHERE   G.title LIKE ? AND
                        G.user_id = U.id AND
                        G.id = L.list_id
                        """
        return db.query(sql, ["%" + name + "%"])
    else:
        sql = """SELECT G.id,
                        G.title,
                        U.username,
                        L.value
                 FROM   giftlists G,
                        users U,
                        list_classes L
                 WHERE  (G.title LIKE ? AND L.title = "Lahjalistan tyyppi" AND L.value = ?) AND
                        G.user_id = U.id AND
                        G.id = L.list_id
                        """
        return db.query(sql, ["%" + name + "%", giftlist_type])

def get_list_passwordhash(list_id):
    sql = "SELECT password_hash FROM giftlists WHERE id = ?"
    return db.query(sql, [list_id])

def list_count():
    sql = "SELECT COUNT(id) FROM giftlists"
    return db.query(sql)[0][0]