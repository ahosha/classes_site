import json

from flask import Blueprint, render_template, request, redirect, url_for

from src.models.lessons.lesson import Lesson
from src.models.teachers.teacher import Teacher

__author__ = 'ahosha'

lesson_blueprint = Blueprint('lessons', __name__)


@lesson_blueprint.route('/')
def index():
    lessons = Lesson.all()
    return render_template('lessons/lesson_index.jinja2', lessons=lessons)


@lesson_blueprint.route('/new', methods=['GET', 'POST'])
def create_lesson():
    if request.method == 'POST':
        name = request.form['name']
        teacherusername = request.form['teacher']
        date = request.form['date']
        time = request.form['time']
        lessontype = request.form['lessontype']

        Lesson(name, teacherusername, date, time, lessontype).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("lessons/new_lesson.jinja2", teachers=Teacher.all(), types=Lesson.get_lesson_types())


@lesson_blueprint.route('/edit/<string:lesson_id>', methods=['GET', 'POST'])
def edit_lesson(lesson_id):
    if request.method == 'POST':
        name = request.form['name']
        teacherusername = request.form['teacherusername']
        date = request.form['date']
        time = request.form['time']
        lessontype = request.form['lessontype']

        lesson = Lesson.get_by_id(lesson_id)

        lesson.name = name
        lesson.teacherusername = teacherusername
        lesson.date = date
        lesson.time = time
        lesson.lessontype = lessontype

        lesson.save_to_mongo()

        return redirect(url_for('.index'))

    else:
        lesson = Lesson.get_by_id(lesson_id)
        teachers = Teacher.all()
        return render_template("lessons/edit_lesson.jinja2", lesson=lesson, teacherusername=lesson.teacherusername, teachers=teachers, types=Lesson.get_lesson_types(), curlessontype=lesson.lessontype)


@lesson_blueprint.route('/delete/<string:lesson_id>')
def delete_lesson(lesson_id):
    lesson = Lesson.get_by_id(lesson_id)
    lesson.delete()
    return redirect(url_for('.index'))


@lesson_blueprint.route('/<string:lesson_id>')
def lesson_page(lesson_id):
    return render_template('lessons/lesson.jinja2', lesson=Lesson.get_by_id(lesson_id))
