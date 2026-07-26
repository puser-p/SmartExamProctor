import sqlite3

def create_database():

    conn = sqlite3.connect("database/exam.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        roll TEXT UNIQUE,

        department TEXT,

        semester TEXT,

        email TEXT,

        phone TEXT,

        gender TEXT

    )
    """)

    conn.commit()

    conn.close()

if __name__ == "__main__":
    create_database()