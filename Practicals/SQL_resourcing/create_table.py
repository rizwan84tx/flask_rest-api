import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
# INTEGER PRIMARY KEY - Create auto incrementing ID for users, so we need to input the ID everytime
cursor.execute(create_user_table)

connection.commit()
connection.close()
