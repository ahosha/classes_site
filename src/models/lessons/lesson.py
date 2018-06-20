import uuid
from src.common.database import Database
import src.models.lessons.constants as LessonConstants
import src.models.lessons.errors as LessonErrors
from src.models.teachers.teacher import Teacher

__author__ = 'ahosha'


class Lesson(object):
    def __init__(self, name, teacherusername, date, time, lessontype, _id=None):
        self.name = name
        teacher = Teacher.get_by_username(teacherusername)
        self.username = teacher.username
        self.date = date
        self.time = time
        self.lessontype = lessontype
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Lesson {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "teacher user name": self.username,
            "date": self.date,
            "time": self.time,
            "lessontype": self.lessontype
        }

    def delete(self):
        Database.remove(LessonConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(LessonConstants.COLLECTION, {})]

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(LessonConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(LessonConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, lesson_name):
        return cls(**Database.find_one(LessonConstants.COLLECTION, {"name": lesson_name}))

    @classmethod
    def get_by_teacher(cls, first_name, last_name):
        try:
            return cls(**Database.find_one(LessonConstants.COLLECTION, {"first_name": first_name, "last_name": last_name}))
        except:
            raise LessonErrors.LessonNotFoundException(
                "lessons for teacher {} {} weren't found".format(first_name, last_name))

    @classmethod
    def find_by_url(cls, url):
        for i in range(0, len(url)+1):
            try:
                lesson = cls.get_by_url_prefix(url[:i])
                return lesson
            except:
                raise LessonErrors.LessonNotFoundException("The URL Prefix used to find the lesson didn't give us any results!")