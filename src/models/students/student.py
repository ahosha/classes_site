import uuid
from src.common.database import Database
import src.models.students.constants as StudentConstants
import src.models.students.errors as StudentErrror
from src.common.utils import Utils

__author__ = 'ahosha'


class Student(object):
    def __init__(self, username, password, firstname, lastname, location, active, abonementtype, abonementstartdate, _id=None):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.location = location
        self.abonementtype = abonementtype
        self.abonementstartdate = abonementstartdate
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id



    def __repr__(self):
        return "<Student username:{} firstname:{} lastname:{}>".format(self.username, self.firstname, self.lastname)

    def json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "location": self.location,
            "abonementtype": self.abonementtype,
            "abonementstartdate": self.abonementstartdate,
            "active": self.active
        }

    def delete(self):
        Database.remove(StudentConstants.COLLECTION, {'_id': self._id})

    def save_to_mongo(self):
        Database.update(StudentConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StudentConstants.COLLECTION, {})]

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StudentConstants.COLLECTION, {"_id": id}))


    @classmethod
    def get_by_username(cls, username):
        return cls(**Database.find_one(StudentConstants.COLLECTION, {"username": username}))

    @classmethod
    def check_before_save(cls, username, password, firstname, lastname, location, active):
        if Utils.isBlank(username) or Utils.isBlank(password) or Utils.isBlank(firstname) or Utils.isBlank(
                lastname) or Utils.isBlank(location) or Utils.isBlank(active):
            raise StudentErrror.StudentWrongInputDataException("one of the input parameters is wrong. Please check ...")

        # if Teacher.get_by_username(username) is not None:
        #     raise TeacherErrror.TeacherExistsException("teacher with username {} already exists".format(username))


