from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

student_bp = Blueprint('student_bp', __name__, template_folder='templates', static_folder='static')

# Path to DB
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "users.db")

# Initialize DB if not exists
if not os.path.exists(DB_PATH):
    from .database import init_db  # assuming init_db is defined in student_login/database.py
    init_db(DB_PATH)

@student_bp.route('/')
def home():
    return render_template('login.html')

@student_bp.route('/login', methods=['POST'])
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
        return redirect(url_for('student_bp.dashboard'))
    else:
        flash("Invalid Student ID or Password")
        return redirect(url_for('student_bp.home'))

@student_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('student_bp.home'))
        except sqlite3.IntegrityError:
            flash("Student ID already exists.")
            return redirect(url_for('student_bp.register'))

    return render_template('register.html')

@student_bp.route('/dashboard')
def dashboard():
    if 'student_id' in session:
        return f"<h2>Welcome {session['student_name']} (ID: {session['student_id']})</h2><br><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for('student_bp.home'))

@student_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('student_bp.home'))
