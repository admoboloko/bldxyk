import sqlite3

# Connect to SQLite
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# Recreate the users table
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    balance REAL
)
''')

print("Table 'users' recreated with the correct schema!")

# Commit changes and close the connection
conn.commit()
conn.close()
