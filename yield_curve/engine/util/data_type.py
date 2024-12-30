from enum import Enum
from typing import Type
from datetime import date


class DataType(Enum):
    INTEGER = int
    LONG = int  # Python's `int` covers both `Integer` and `Long`.
    DOUBLE = float
    LOCAL_DATE = date
    STRING = str

    def __init__(self, clazz: Type):
        self.clazz = clazz

    def get_clazz(self) -> Type:
        return self.clazz
