from typing import Dict, Optional, Set
from collections import defaultdict
from yield_curve.engine.util.abs_data_row import DataRow
from yield_curve.engine.util.abs_data_field import DataField
from yield_curve.engine.util.abs_database import DataBase
from yield_curve.engine.util.data_row_immutable import DataRowImmutable


class DataBaseImmutable(DataBase):
    def __init__(self, name_to_id_row: Dict[str, Dict[int, DataRowImmutable]]):
        # Deep copy for immutability
        self.name_to_id_row = {
            table: dict(rows) for table, rows in name_to_id_row.items()
        }

    def get_data_row(self, table_name: str, row_id: int) -> DataRowImmutable:
        id_to_row = self.name_to_id_row.get(table_name)
        if id_to_row is None:
            raise ValueError(f"Invalid tableName: {table_name}")
        data_row = id_to_row.get(row_id)
        if data_row is None:
            raise ValueError(f"Invalid rowId for table {table_name}: {row_id}")
        return data_row

    def find_data_row(self, table_name: str, row_id: int) -> Optional[DataRowImmutable]:
        id_to_row = self.name_to_id_row.get(table_name)
        if id_to_row:
            return id_to_row.get(row_id)
        return None

    def get_all_by_table(self, table_name: str) -> Set[int]:
        id_to_row = self.name_to_id_row.get(table_name)
        if id_to_row:
            return set(id_to_row.keys())
        return set()

    def index(self, table_name: str, field_name: str) -> Dict[DataField, int]:
        id_to_row = self.name_to_id_row.get(table_name)
        if id_to_row is None:
            raise ValueError(f"Invalid tableName: {table_name}")

        index_map = {}
        for row_id, data_row in id_to_row.items():
            field_value = data_row.get_data_field(field_name)
            if field_value is not None:
                index_map[field_value] = row_id
        return index_map

    def index_non_unique(self, table_name: str, field_name: str) -> Dict[DataField, Set[int]]:
        id_to_row = self.name_to_id_row.get(table_name)
        if id_to_row is None:
            raise ValueError(f"Invalid tableName: {table_name}")

        index_map = defaultdict(set)
        for row_id, data_row in id_to_row.items():
            field_value = data_row.get_data_field(field_name)
            if field_value is not None:
                index_map[field_value].add(row_id)
        return dict(index_map)

    @staticmethod
    def builder():
        return DataBaseImmutable.Builder()

    class Builder:
        def __init__(self):
            self.name_to_id_row = defaultdict(dict)

        def with_data_row(self, table_name: str, data_row: DataRowImmutable):
            if table_name and data_row:
                row_id = data_row.get_row_id()
                if row_id is not None:
                    self.name_to_id_row[table_name][row_id] = data_row
            return self

        def build(self) -> "DataBaseImmutable":
            return DataBaseImmutable(self.name_to_id_row)
