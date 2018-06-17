import json
from flask import Blueprint, render_template, request, redirect, url_for
from src.models.teachers.teacher import Teacher
import src.models.teachers.errors as TeacherErrrors
from src.common.utils import  Utils


teacher_blueprint = Blueprint('teachers', __name__)


@teacher_blueprint.route('/')
def index():
    teachers = Teacher.all()
    return render_template('teachers/teacher_index.jinja2', teachers=teachers)



@teacher_blueprint.route('/new', methods=['GET', 'POST'])
def create_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        location = request.form['location']
        active = request.form['active']

        try:
            Teacher.check_before_save(username, password,firstname,lastname,location, active)
        except TeacherErrrors.TeacherWrongInputDataException as e:
            return e.message
        except TeacherErrrors.TeacherExistsException as e:
            return e.message

        Teacher(username, password, firstname, lastname, location, active).save_to_mongo()
        return redirect(url_for(".index"))

    return render_template("teachers/new_teacher.jinja2")


@teacher_blueprint.route('/edit/<string:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        location = request.form['location']
        active = request.form['active']

        teacher = Teacher.get_by_id(teacher_id)

        teacher.username = username
        teacher.password = password
        teacher.firstname = firstname
        teacher.lastname = lastname
        teacher.location = location
        teacher.active = active

        teacher.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("teachers/edit_teacher.jinja2", teacher=Teacher.get_by_id(teacher_id))


@teacher_blueprint.route('/delete/<string:teacher_id>')
def delete_teacher(teacher_id):
    Teacher.get_by_id(teacher_id).delete()
    return redirect(url_for('.index'))


@teacher_blueprint.route('/<string:teacher_username>')
def teacher_page(teacher_username):
    teacher = Teacher.get_by_username(teacher_username)
    if teacher is not None:
        return render_template('teachers/teacher.jinja2', teacher=teacher)
    else:
        return "wrong user name"
