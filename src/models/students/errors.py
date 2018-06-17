
class StudentException(Exception):
    def __init__(self, message):
        self.message = message


class StudentNotFoundException(StudentException):
    pass


class StudentWrongInputDataException(StudentException):
    pass


class StudentExistsException(StudentException):
    pass