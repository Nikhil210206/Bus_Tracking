from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB_PATH = os.path.join("database", "users.db")

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
        session['student_id'] = student_id
        session['student_name'] = user[0]
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid Student ID or Password")
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        password = request.form['password']

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (student_id, name, password) VALUES (?, ?, ?)", 
                          (student_id, name, password))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.")
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash("Student ID already exists.")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'student_id' in session:
        return f"<h2>Welcome {session['student_name']} (ID: {session['student_id']})</h2><br><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
