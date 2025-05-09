import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Add a sample user (username: test, password: 1234)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("test", "1234"))

conn.commit()
conn.close()
