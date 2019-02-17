import sqlite3

connection = sqlite3.connect('data.db') #data.db - DB to connect
cursor = connection.cursor()

#create_table = "CREATE TABLE users (id int, username text, password text)" #Schema
#cursor.execute(create_table)

#user = (1, 'Rizwan', 'abc') #Create a user info
#insert_query = "INSERT INTO users VALUES (?, ?, ?)" #Inserting the user data into users table
#cursor.execute(insert_query, user) # Executing insert_query

# Inserting multiple user
#user_list = [
#    (2, 'Sana', 'abc'),
#    (3, 'Yahya', 'abc'),
#    (4, 'Hafsa', 'abc')
#]
#cursor.executemany(insert_query, user_list)

# Selecting and View data in DB
select_query = "SELECT * FROM users WHERE username=?"
user = 'Rizwan'
run_query = cursor.execute(select_query, (user,))
user = next(filter(lambda x:x[1] == user, run_query), None)
if user is None:
    print ('xxx')
else:
    print ('yyy')
#for row in cursor.execute(select_query, ('Sana',)):
#    print(row)

connection.commit() #Saving the changes
connection.close() # closes the connection
