import sqlite3

conn = sqlite3.connect("database/exam.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()