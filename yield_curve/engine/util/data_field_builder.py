from typing import Any, Type

from yield_curve.engine.util.data_field_immutable import DataFieldImmutable
from yield_curve.engine.util.data_type import DataType


class DataFieldBuilder:
    def __init__(self):
        self._name = None
        self._data_type = None
        self._value = None

    def with_name(self, name: str) -> "DataFieldBuilder":
        self._name = name
        return self

    def with_data_type(self, data_type: DataType) -> "DataFieldBuilder":
        self._data_type = data_type
        return self

    def with_value(self, value: Any) -> "DataFieldBuilder":
        self._value = value
        return self

    def build(self) -> DataFieldImmutable:
        return DataFieldImmutable(self._name, self._data_type, self._value)

    @staticmethod
    def new_builder() -> "DataFieldBuilder":
        return DataFieldBuilder()
