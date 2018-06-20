import uuid
from src.common.database import Database
import src.models.attendance.constants as AttendanceConstants
import src.models.attendance.errors as AttendanceErrors

__author__ = 'ahosha'


class Attendance(object):
    def __init__(self, studentname, teacherusername, date, time, lessonname, _id=None):
        self.studentname = studentname
        self.teacherusername = teacherusername
        self.date = date
        self.time = time
        self.lessonname = lessonname
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Attendance studentname:{} teacherusername:{} date:{} time:{} lessonname:{}>".format(self.studentname, self.teacherusername, self.date, self.time, self.lessonname)

    def json(self):
        return {
            "_id": self._id,
            "studentname": self.studentname,
            "teacherusername": self.teacherusername,
            "date": self.date,
            "time": self.time,
            "lessonname": self.lessonname
        }

    def delete(self):
        Database.remove(AttendanceConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(AttendanceConstants.COLLECTION, {})]

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(AttendanceConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(AttendanceConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_sudent(cls, studentname):
        try:
            return cls(**Database.find_one(AttendanceConstants.COLLECTION, {"studentname": studentname}))
        except:
            raise AttendanceErrors.AttendanceNotFoundException(
                "Attendances for student: {} weren't found".format(studentname))

    @classmethod
    def get_by_teacher(cls, teacherusername):
        try:
            return cls(**Database.find_one(AttendanceConstants.COLLECTION, {"teacherusername": teacherusername}))
        except:
            raise AttendanceErrors.AttendanceNotFoundException(
                "Attendances for teacher: {} weren't found".format(teacherusername))


