from enum import Enum


class State(str, Enum):
    PENDING = "PENDING"
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'
