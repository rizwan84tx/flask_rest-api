import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
# INTEGER PRIMARY KEY - Create auto incrementing ID for users, so we need to input the ID everytime
cursor.execute(create_user_table)

create_item_table = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
# real - float data type
cursor.execute(create_item_table)

#query = "INSERT INTO items VALUES ('phone', 11000.99)"
#cursor.execute(query)


connection.commit()
connection.close()
