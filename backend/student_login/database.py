import sqlite3
import os

def init_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            name TEXT,
            password TEXT
        );
    ''')
    cursor.execute("INSERT OR IGNORE INTO students (student_id, name, password) VALUES (?, ?, ?)",
                   ("SRM123", "Nikhil", "pass123"))
    conn.commit()
    conn.close()
