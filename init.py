import db

list_types = ["Hääjuhlan lahjatoivelista", "Syntymäpäiväjuhlan lahjatoivelista", "Valmistujaisten lahjatoivelista", "Muu lahjatoivelista"]

if __name__ == "__main__":
    sql = "INSERT INTO classes (title, value) VALUES ('type', ?)"
    for list_type in list_types:
        db.execute(sql, [list_type])