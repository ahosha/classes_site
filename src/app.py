from flask import Flask, render_template
from src.common.database import Database

__author__ = 'ahosha'

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.teachers.views import teacher_blueprint
from src.models.students.views import student_blueprint
from src.models.lessons.views import lesson_blueprint
from src.models.attendance.views import attendance_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(teacher_blueprint, url_prefix="/teachers")
app.register_blueprint(student_blueprint, url_prefix="/students")
app.register_blueprint(lesson_blueprint, url_prefix="/lessons")
app.register_blueprint(attendance_blueprint, url_prefix="/attendances")