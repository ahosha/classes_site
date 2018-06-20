__author__ = 'ahosha'


class AttendanceException(Exception):
    def __init__(self, message):
        self.message = message


class AttendanceNotFoundException(AttendanceException):
    pass