import db

list_types = ["Hääjuhla", "Syntymäpäiväjuhla", "Valmistujaiset", "Muu"]

def get_classes():
    sql = "SELECT title, value from classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes
