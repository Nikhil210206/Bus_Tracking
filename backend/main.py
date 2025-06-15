from flask import Flask
from student_login.app import student_bp
from driver_login.app import driver_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.register_blueprint(student_bp)
app.register_blueprint(driver_bp, url_prefix='/driver')

if __name__ == '__main__':
    app.run(debug=True)
