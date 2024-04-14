from enum import Enum


class Role(str, Enum):
    USER = 'USER'
    STUDENT = 'STUDENT'
    MODERATOR = 'MODERATOR'
    CAPTAIN = 'CAPTAIN'
    ADMIN = 'ADMIN'

class TeacherRole(str, Enum):
    LECTURER = 'LECTURER'
    LABORANT = 'LABORANT'
    PRACTICIAN = 'PRACTICIAN'
    EXAMINER = 'EXAMINER'
    OTHER = 'OTHER'
