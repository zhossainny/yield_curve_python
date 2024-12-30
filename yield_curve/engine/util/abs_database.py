from abc import ABC, abstractmethod
from typing import Optional, Set, Dict


class DataBase(ABC):
    @abstractmethod
    def get_data_row(self, table_name: str, row_id: int):
        pass

    @abstractmethod
    def find_data_row(self, table_name: str, row_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_all_by_table(self, table_name: str) -> Set[int]:
        pass

    @abstractmethod
    def index(self, table_name: str, field_name: str) -> Dict[str, int]:
        pass

    @abstractmethod
    def index_non_unique(self, table_name: str, field_name: str) -> Dict[str, Set[int]]:
        pass
