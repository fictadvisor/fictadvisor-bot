from enum import Enum


class PollSort(str, Enum):
    ID = 'ID'
    FIRSTNAME = 'FIRSTNAME'
    MIDDLENAME = 'MIDDLENAME'
    LASTNAME = 'LASTNAME'
    RATING = 'RATING'


class PollOrder(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class QuestionType(str, Enum):
    TEXT = 'TEXT'
    SCALE = 'SCALE'
    TOGGLE = 'TOGGLE'


class DisplayType(str, Enum):
    AMOUNT = 'AMOUNT'
    RADAR = 'RADAR'
    CIRCLE = 'CIRCLE'
