from enum import Enum


class Role(str, Enum):
    USER = 'USER'
    STUDENT = 'STUDENT'
    MODERATOR = 'MODERATOR'
    CAPTAIN = 'CAPTAIN'
    ADMIN = 'ADMIN'
