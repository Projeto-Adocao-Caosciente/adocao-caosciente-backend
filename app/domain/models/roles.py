from enum import Enum

class Role(int, Enum):
    ADMIN = 0
    ONG = 1
    USER = 2