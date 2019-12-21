import sqlite3


def initusers():
    connection = sqlite3.connect("data.database")
    cursor = connection.cursor()

    print()
    print("Creating table user...")
    create_table = "CREATE TABLE IF NOT EXISTS users (" \
                   "id INTEGER PRIMARY KEY, " \
                   "username TEXT, " \
                   "password TEXT, " \
                   "admin INTEGER" \
                   ")"
    cursor.execute(create_table)

    print("Inserting users...", end=" ")
    users = [(1, "admin", "admin123", True),
             (2, "jane", "jane123", False),
             (3, "john", "john123", False)]

    insert_query = "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)"
    cursor.executemany(insert_query, users)
    print("Done.")

    count_query = "SELECT COUNT(*) FROM users"
    print("Users count:", cursor.execute(count_query).fetchone()[0])

    print()
    print("List of users:")
    select_query = "SELECT * FROM users"
    for row in cursor.execute(select_query):
        print(row)

    connection.commit()
    connection.close()
    print("user table initialization complete")


def initItems():
    connection = sqlite3.connect("data.database")
    cursor = connection.cursor()

    print()
    print("Creating table items...")
    create_table = "CREATE TABLE IF NOT EXISTS items (" \
                   "id INTEGER PRIMARY KEY, " \
                   "name TEXT COLLATE NOCASE, " \
                   "price REAL" \
                   ")"
    cursor.execute(create_table)

    print("Inserting items...", end=" ")
    items = [(1, "Rotisserie Chicken", 4.99),
             (2, "Dildo", 12.98),
             (3, "Vibrator", 27.95)]
    insert_query = "INSERT OR IGNORE INTO items VALUES (?, ?, ?)"
    cursor.executemany(insert_query, items)
    print("Done.")

    count_query = "SELECT COUNT(*) FROM items"
    print("Items count:", cursor.execute(count_query).fetchone()[0])
    print()
    print("List of items:")
    select_query = "SELECT * FROM items"
    for row in cursor.execute(select_query):
        print(row)

    connection.commit()
    connection.close()
    print("Items table initialization complete")


if __name__ == "__main__":
    initusers()
    initItems()
