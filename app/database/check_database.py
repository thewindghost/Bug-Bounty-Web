import sqlite3

DATABASE_PATH = "./database.db"

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

print("[+] Tables List:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for t in tables:
    print(" -", t[0])

print("\n[+] Tables Data 'admins' and 'users':")
cursor.execute("SELECT * FROM admins UNION SELECT * FROM users;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
