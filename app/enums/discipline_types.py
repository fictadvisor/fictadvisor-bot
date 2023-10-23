from enum import Enum


class DisciplineTypes(str, Enum):
    LECTURE = 'LECTURE'
    PRACTICE = 'PRACTICE'
    LABORATORY = 'LABORATORY'
    CONSULTATION = 'CONSULTATION'
    WORKOUT = 'WORKOUT'
    EXAM = 'EXAM'
