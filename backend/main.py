from flask import Flask
from student_login.app import student_bp
from driver_login.app import driver_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Register Blueprints
app.register_blueprint(student_bp)
app.register_blueprint(driver_bp)

if __name__ == '__main__':
    app.run(debug=True)
