from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_PATH = os.path.join("database", "users.db")

# Ensure DB exists
if not os.path.exists(DB_PATH):
    from database import init_db
    init_db(DB_PATH)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    student_id = request.form['student_id']
    password = request.form['password']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE student_id=? AND password=?", (student_id, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"<h2>Welcome {user[0]}!</h2>"
    else:
        flash("Invalid Student ID or Password")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
