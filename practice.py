import sqlite3

# Establish a connection and cursor to the SQLite database
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Query all the database for specific data based on a condition
cursor.execute("SELECT * FROM events WHERE date='2088.10.15'")
result = cursor.fetchall()
print(type(result))
print(result)
# Query certain columns in the database for specific data based on a condition
cursor.execute("SELECT band, date FROM events WHERE date='2088.10.15'")
result = cursor.fetchall()
print(type(result))
print(result)

# Insert new rows into the database
new_rows = [('Cats', 'Cat City', '2088.10.17'),
            ('Hens', 'Hen City', '2088.10.17')]

cursor.executemany("INSERT INTO events VALUES(?, ?, ?)", new_rows)
connection.commit()

# Query all the database
cursor.execute("SELECT * FROM events")
result = cursor.fetchall()
print(type(result))
print(result)
