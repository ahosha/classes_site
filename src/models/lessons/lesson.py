import uuid
from src.common.database import Database
import src.models.lessons.constants as LessonConstants
import src.models.lessons.errors as LessonErrors
from src.models.teachers.teacher import Teacher
from src.common.const import LESSON_TYPES

__author__ = 'ahosha'


class Lesson(object):
    def __init__(self, name, teacherusername, date, time, lessontype, _id=None):
        self.name = name
        self.teacherusername = teacherusername
        self.date = date
        self.time = time
        self.lessontype = lessontype
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Lesson name:{} teacherusername:{} date:{} time:{} lessontype:{}>".format(self.name, self.teacherusername, self.date, self.time, self.lessontype)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "teacherusername": self.teacherusername,
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
    def get_by_teacher(cls, teacherusername):
        try:
            return cls(**Database.find_one(LessonConstants.COLLECTION, {"teacherusername": teacherusername}))
        except:
            raise LessonErrors.LessonNotFoundException(
                "lessons for teacher: {} weren't found".format(teacherusername))

    @staticmethod
    def get_lesson_types():
        return LESSON_TYPES
