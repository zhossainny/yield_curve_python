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

from enum import Enum


class QuoteField(Enum):
    PRICE = "PRICE"
    CONVEXITY_ADJ = "CONVEXITY_ADJ"


class Quote:
    def __init__(self, field: QuoteField, value: float):
        """
        Initializes the Quote object with a field and value.
        :param field: The field of the quote (e.g., PRICE, CONVEXITY_ADJ).
        :param value: The value of the quote.
        """
        self._field = field
        self._value = value

    def get_field(self) -> QuoteField:
        """
        Gets the field of the quote.
        :return: The field of the quote.
        """
        return self._field

    def get_value(self) -> float:
        """
        Gets the value of the quote.
        :return: The value of the quote.
        """
        return self._value
