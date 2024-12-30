from typing import Dict, Optional

from yield_curve.engine.util.abs_data_row import DataRow
from yield_curve.engine.util.data_field_immutable import DataField


class DataRowImmutable(DataRow):
    def __init__(self, row_id: int, name_to_field: Dict[str, DataField]):
        self._row_id = row_id
        self._name_to_field = name_to_field.copy()  # Ensures immutability by creating a copy

    def get_row_id(self) -> int:
        return self._row_id

    def get_data_field(self, name: str) -> DataField:
        if name not in self._name_to_field:
            raise ValueError(f"No data field found for name: {name}")
        return self._name_to_field[name]

    def find_data_field(self, name: str) -> Optional[DataField]:
        return self._name_to_field.get(name)

    def to_builder(self) -> "DataRowBuilder":
        builder = DataRowBuilder()
        builder.with_row_id(self._row_id)
        for field in self._name_to_field.values():
            builder.with_data_field(field)
        return builder

    @staticmethod
    def builder() -> "DataRowBuilder":
        return DataRowBuilder()


class DataRowBuilder:
    def __init__(self):
        self._row_id = None
        self._name_to_field: Dict[str, DataField] = {}

    def with_row_id(self, row_id: int) -> "DataRowBuilder":
        self._row_id = row_id
        return self

    def with_data_field(self, data_field: DataField) -> "DataRowBuilder":
        if data_field is not None:
            self._name_to_field[data_field.get_name()] = data_field
        return self

    def build(self) -> DataRowImmutable:
        if self._row_id is None:
            raise ValueError("Row ID must be set before building a DataRowImmutable.")
        return DataRowImmutable(self._row_id, self._name_to_field)
