import json
from flask import Blueprint, render_template, request, redirect, url_for
from src.models.students.student import Student
import src.models.students.errors as StudentErrrors
import src.models.users.decorators as user_decorators

student_blueprint = Blueprint('students', __name__)


@student_blueprint.route('/')
@user_decorators.requires_login
def index():
    students = Student.all()
    return render_template('students/students_index.jinja2', students=students)


@student_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_student():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        location = request.form['location']
        abonementtype = request.form['abonementtype']
        abonementstartdate = request.form['abonementstartdate']
        active = request.form['active']


        try:
            Student.check_before_save(username, password, firstname, lastname, location, abonementtype, abonementstartdate, active)
        except StudentErrrors.StudentWrongInputDataException as e:
            return e.message
        except StudentErrrors.StudentExistsException as e:
            return e.message

        Student(username, password, firstname, lastname, location, abonementtype, abonementstartdate, active).save_to_mongo()
        return redirect(url_for('.index'))

    return render_template('students/new_student.jinja2')


@student_blueprint.route('/edit/<string:student_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_student(student_id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        location = request.form['location']
        abonementtype = request.form['abonementtype']
        abonementstartdate = request.form['abonementstartdate']
        active = request.form['active']

        student = Student.get_by_id(student_id)

        student.username = username
        student.password = password
        student.firstname = firstname
        student.lastname = lastname
        student.location = location
        student.abonementtype = abonementtype
        student.abonementstartdate = abonementstartdate
        student.active = active

        student.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("students/edit_student.jinja2", student=Student.get_by_id(student_id))


@student_blueprint.route('/delete/<string:student_id>')
@user_decorators.requires_login
def delete_student(student_id):
    Student.get_by_id(student_id).delete()
    return redirect(url_for('.index'))


@student_blueprint.route('/<string:student_username>')
@user_decorators.requires_login
def student_page(student_username):
    student = Student.get_by_username(student_username)
    if student is not None:
        return render_template('students/student.jinja2', student=student)
    else:
        return "wrong user name"
