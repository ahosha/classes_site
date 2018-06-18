__author__ = 'ahosha'


class LessonException(Exception):
    def __init__(self, message):
        self.message = message


class LessonNotFoundException(LessonException):
    pass