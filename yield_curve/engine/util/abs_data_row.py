from abc import ABC, abstractmethod
from typing import Optional
from yield_curve.engine.util.data_field_immutable import DataField


class DataRow(ABC):
    @abstractmethod
    def get_row_id(self) -> int:
        pass

    @abstractmethod
    def get_data_field(self, name: str) -> DataField:
        pass

    @abstractmethod
    def find_data_field(self, name: str) -> Optional[DataField]:
        pass
