import db
from classes import list_types

if __name__ == "__main__":
    sql = "INSERT INTO classes (title, value) VALUES ('Lahjalistan tyyppi', ?)"
    for list_type in list_types:
        db.execute(sql, [list_type])