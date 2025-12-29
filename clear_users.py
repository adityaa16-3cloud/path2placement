import sqlite3

conn = sqlite3.connect("database/users.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users;")

conn.commit()
conn.close()

print("✅ users table cleared successfully")
