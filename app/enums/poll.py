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