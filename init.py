import db
from classes import list_types

if __name__ == "__main__":
    sql = "INSERT INTO classes (title, value) VALUES ('Lahjalistan tyyppi', ?)"
    for list_type in list_types:
        db.execute(sql, [list_type])
    
    sql = "CREATE INDEX idx_gls_title_uid ON giftlists (title, user_id)"
    db.execute(sql)
    sql = "CREATE INDEX idx_gifts_glsid ON gifts (giftlist_id)"
    db.execute(sql)