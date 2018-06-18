import uuid
from src.common.database import Database
import src.models.lessons.constants as LessonConstants
import src.models.lessons.errors as LessonErrors

__author__ = 'ahosha'


class Lesson(object):
    def __init__(self, name, teacherid, date, time, lessontype, _id=None):
        self.name = name
        self.teacher = teacherid
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
            "teacher": self.teacher,
            "date": self.date,
            "time": self.time,
            "lessontype": self.lessontype,
            "query": self.query
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
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(LessonConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        for i in range(0, len(url)+1):
            try:
                lesson = cls.get_by_url_prefix(url[:i])
                return lesson
            except:
                raise LessonErrors.LessonNotFoundException("The URL Prefix used to find the lesson didn't give us any results!")