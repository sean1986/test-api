#!/usr/bin/env python

import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"
# cursor.execute(create_table)

insert_user = "INSERT INTO users VALUES (?, ?, ?)"

user = (1, "sean", "Passw0rd")
# cursor.execute(insert_user, user)
# connection.commit()

users = [
    (2, "jane", "Passw0rd"),
    (3, "betsy", "Passw0rd"),
]
# cursor.executemany(insert_user, users)
# connection.commit()

select_users = "SELECT * FROM users"
for row in cursor.execute(select_users):
    print(row)

connection.close()
