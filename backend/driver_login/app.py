from flask import Blueprint, render_template, request, redirect, url_for, flash

driver_bp = Blueprint('driver_bp', __name__, url_prefix='/driver', template_folder='templates')

@driver_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        password = request.form['password']
        # Dummy check
        if driver_id == 'driver1' and password == 'pass123':
            return "Driver Logged In"
        else:
            flash("Invalid credentials")
            return redirect(url_for('driver_bp.login'))

    return render_template('login.html')

@driver_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle driver registration
        return "Driver Registered Successfully!"
    return render_template('register.html')
