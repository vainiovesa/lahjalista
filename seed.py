import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM giftlists")
db.execute("DELETE FROM gifts")

user_count = 10000
list_count = 10**6
gift_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, list_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO giftlists (title, user_id) VALUES (?, ?)",
               ["list" + str(i), user_id])

for i in range(1, gift_count + 1):
    user_id = random.randint(1, user_count)
    giftlist_id = random.randint(1, list_count)
    db.execute("""INSERT INTO gifts (title, getter_id, giftlist_id)
                  VALUES (?, ?, ?)""",
               ["gift" + str(i), user_id, giftlist_id])

db.commit()
db.close()
