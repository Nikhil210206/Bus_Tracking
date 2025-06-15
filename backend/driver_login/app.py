from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

driver_bp = Blueprint('driver_bp', __name__, template_folder='templates')

DB_PATH = os.path.join(os.path.dirname(__file__), "drivers.db")

# Create DB and table if not exists
def init_driver_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_driver_db()

@driver_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM drivers WHERE driver_id=? AND password=?", (driver_id, password))
        driver = cursor.fetchone()
        conn.close()

        if driver:
            session['driver_id'] = driver_id
            session['driver_name'] = driver[0]
            return f"<h2>Welcome Driver {driver[0]} (ID: {driver_id})</h2><br><a href='/driver/logout'>Logout</a>"
        else:
            flash("Invalid Driver ID or Password")
            return redirect(url_for('driver_bp.login'))

    return render_template('login.html')

@driver_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        name = request.form['name']
        password = request.form['password']

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO drivers (driver_id, name, password) VALUES (?, ?, ?)",
                          (driver_id, name, password))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.")
            return redirect(url_for('driver_bp.login'))
        except sqlite3.IntegrityError:
            flash("Driver ID already exists.")
            return redirect(url_for('driver_bp.register'))

    return render_template('register.html')

@driver_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('driver_bp.login'))
