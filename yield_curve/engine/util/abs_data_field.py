from abc import ABC, abstractmethod
from typing import Any, Optional, Union
from datetime import date


class DataField(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_data_type(self) -> str:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass

    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def find_value(self) -> Optional[Any]:
        pass

    def get_local_date(self) -> date:
        pass