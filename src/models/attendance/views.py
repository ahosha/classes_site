import json

from flask import Blueprint, render_template, request, redirect, url_for
from src.models.students.student import Student
from src.models.attendance.attendance import Attendance
from src.models.teachers.teacher import Teacher
from src.models.lessons.lesson import Lesson

__author__ = 'ahosha'

attendance_blueprint = Blueprint('attendances', __name__)


@attendance_blueprint.route('/')
def index():
    attendances = Attendance.all()
    return render_template('attendance/attendance_index.jinja2', attendances=attendances)


@attendance_blueprint.route('/new', methods=['GET', 'POST'])
def create_attendance():
    if request.method == 'POST':
        studentname = request.form['studentname']
        teacherusername = request.form['teacherusername']
        date = request.form['date']
        time = request.form['time']
        lessonname = request.form['lessonname']

        Attendance(studentname, teacherusername, date, time, lessonname).save_to_mongo()

        return redirect(url_for('.index'))

    else:
        teachers = Teacher.all()
        students = Student.all()
        lessons = Lesson.all()
    return render_template("attendance/new_attendance.jinja2", teachers=teachers, students=students, lessons=lessons)


@attendance_blueprint.route('/edit/<string:attendance_id>', methods=['GET', 'POST'])
def edit_attendance(attendance_id):
    if request.method == 'POST':
        studentname = request.form['studentname']
        teacherusername = request.form['teacherusername']
        date = request.form['date']
        time = request.form['time']
        lessonname = request.form['lessonname']

        attendance = Attendance.get_by_id(attendance_id)

        attendance.studentname = studentname
        attendance.teacherusername = teacherusername
        attendance.date = date
        attendance.time = time
        attendance.lessonname = lessonname

        attendance.save_to_mongo()

        return redirect(url_for('.index'))

    else:
        attendance = Attendance.get_by_id(attendance_id)
        # teacher = Teacher.get_by_username(attendance.teacherusername)
        # student = Student.get_by_username(attendance.studentname)
        # lesson = Lesson.get_by_name(attendance.lesson)
        return render_template("attendance/edit_attendance.jinja2", attendance=attendance,
                               teachers=Teacher.all(),
                               students=Student.all(),
                               lessons=Lesson.all(),
                               teacherusername=attendance.teacherusername,
                               student=attendance.studentname,
                               curlessonname=attendance.lessonname)


@attendance_blueprint.route('/delete/<string:attendance_id>')
def delete_attendance(attendance_id):
    attendance = Attendance.get_by_id(attendance_id)
    attendance.delete()
    return redirect(url_for('.index'))


@attendance_blueprint.route('/<string:attendance_id>')
def attendance_page(attendance_id):
    return render_template('attendance/attendance.jinja2', attendance=Attendance.get_by_id(attendance_id))
