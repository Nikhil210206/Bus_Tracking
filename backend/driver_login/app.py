from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

driver_bp = Blueprint('driver', __name__, template_folder='templates')

DB_PATH = os.path.join(os.path.dirname(__file__), 'driver_users.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS drivers (
                        driver_id TEXT PRIMARY KEY,
                        name TEXT,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()

init_db()

@driver_bp.route('/login', methods=['GET', 'POST'])
def driver_login():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM drivers WHERE driver_id=? AND password=?", (driver_id, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['driver_id'] = driver_id
            session['driver_name'] = user[0]
            return f"<h2>Welcome Driver {user[0]} (ID: {driver_id})</h2><a href='/driver/logout'>Logout</a>"
        else:
            flash("Invalid Driver ID or Password")
            return redirect(url_for('driver.driver_login'))

    return render_template('login.html')

@driver_bp.route('/register', methods=['GET', 'POST'])
def driver_register():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        name = request.form['name']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO drivers (driver_id, name, password) VALUES (?, ?, ?)",
                        (driver_id, name, password))
            conn.commit()
            flash("Driver registered successfully! Please login.")
        except sqlite3.IntegrityError:
            flash("Driver ID already exists.")
            return redirect(url_for('driver.driver_register'))
        finally:
            conn.close()

        return redirect(url_for('driver.driver_login'))

    return render_template('register.html')

@driver_bp.route('/logout')
def driver_logout():
    session.pop('driver_id', None)
    session.pop('driver_name', None)
    flash("Driver logged out successfully.")
    return redirect(url_for('driver.driver_login'))
