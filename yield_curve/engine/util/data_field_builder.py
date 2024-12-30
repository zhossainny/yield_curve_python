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
