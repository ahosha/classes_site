import uuid
from src.common.database import Database
import src.models.teachers.constants as TeacherConstants
import src.models.teachers.errors as TeacherErrror
from src.common.utils import Utils

__author__ = 'ahosha'


class Teacher(object):
    def __init__(self, username, password, firstname, lastname, location, active, _id=None):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.location = location
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "'_id':{} 'username':{} 'password':{} 'firstname':{} 'lastname':{} 'location':{} 'active':{}>".format(
            self._id,
            self.username, self.password,
            self.firstname, self.lastname,
            self.location, self.active)

    def json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "location": self.location,
            "active": self.active
        }

    def delete(self):
        Database.remove(TeacherConstants.COLLECTION, {'_id': self._id})

    def save_to_mongo(self):
        Database.update(TeacherConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def all(cls):
        # teachtoret = []
        # teachers = Database.find(TeacherConstants.COLLECTION, {})
        # for teacher in teachers:
        #     teach = Teacher(teacher['username'], teacher['password'], teacher['firstname'], teacher['lastname'],
        #                     teacher['location'], teacher['active'], teacher['_id'])
        #     teachtoret.append(teach)
        # #return [cls(**elem) for elem in teachers]
        # return teachtoret

        return [cls(**elem) for elem in Database.find(TeacherConstants.COLLECTION, {})]

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(TeacherConstants.COLLECTION, {"_id": id}))

    @classmethod
    def get_by_username(cls, username):
        return cls(**Database.find_one(TeacherConstants.COLLECTION, {"username": username}))

    @classmethod
    def check_before_save(cls, username, password, firstname, lastname, location, active):
        if Utils.isBlank(username) or Utils.isBlank(password) or Utils.isBlank(firstname) or Utils.isBlank(
                lastname) or Utils.isBlank(location) or Utils.isBlank(active):
            raise TeacherErrror.TeacherWrongInputDataException("one of the input parameters is wrong. Please check ...")

        # if Teacher.get_by_username(username) is not None:
        #     raise TeacherErrror.TeacherExistsException("teacher with username {} already exists".format(username))

    """

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(TeacherConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):

        for i in range(0, len(url) + 1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise TeacherErrors.TeacherNotFoundException(
                    "The URL Prefix used to find the store didn't give us any results!")
"""
