# Licensed under the Apache License, Version 2.0
# Copyright 2024 Zahid Hossain <zhossainny@gmail.com>
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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