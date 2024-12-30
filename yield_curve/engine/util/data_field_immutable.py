from typing import Any, Optional
from datetime import date

from yield_curve.engine.util.abs_data_field import DataField
from yield_curve.engine.util.data_type import DataType


class DataFieldImmutable(DataField):
    def __init__(self, name: str, data_type: DataType, value: Any):
        if not name:
            raise ValueError("Invalid name: Name cannot be empty or null.")
        if not isinstance(data_type, DataType):
            raise ValueError(f"Invalid data type: {data_type}")
        if value is not None and not self._validate_type(data_type, value):
            raise ValueError(f"Type mismatch: Expected {data_type.name}, got {type(value).__name__}")
        self._name = name
        self._data_type = data_type
        self._value = value

    def get_name(self) -> str:
        return self._name

    def get_data_type(self) -> DataType:
        return self._data_type

    def is_null(self) -> bool:
        return self._value is None

    def get_value(self) -> Any:
        if self.is_null():
            raise ValueError("Value is null.")
        return self._value

    def find_value(self) -> Optional[Any]:
        return self._value

    def get_local_date(self) -> date:
        if self._data_type != DataType.LOCAL_DATE:
            raise ValueError(f"Field is not of type LOCAL_DATE: {self._data_type}")
        return self._value

    @staticmethod
    def _validate_type(data_type: DataType, value: Any) -> bool:
        type_mapping = {
            DataType.INTEGER: int,
            DataType.LONG: int,  # In Python, `int` handles both `int` and `long`.
            DataType.DOUBLE: float,
            DataType.STRING: str,
            DataType.LOCAL_DATE: date,
        }
        expected_type = type_mapping.get(data_type)
        return isinstance(value, expected_type)
