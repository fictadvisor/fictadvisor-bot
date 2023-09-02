from enum import Enum


class States(str, Enum):
    PENDING = "PENDING"
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'
