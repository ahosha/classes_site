
class TeacherException(Exception):
    def __init__(self, message):
        self.message = message


class TeacherNotFoundException(TeacherException):
    pass


class TeacherWrongInputDataException(TeacherException):
    pass


class TeacherExistsException(TeacherException):
    pass