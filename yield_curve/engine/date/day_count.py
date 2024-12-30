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

from datetime import date
from typing import Callable


class DayCount:
    """
    Represents various day count conventions for calculating year fractions.
    """
    def __init__(self, year_fraction_function: Callable[[date, date], float]):
        """
        Initialize with a specific year fraction calculation function.
        :param year_fraction_function: Function to calculate year fractions.
        """
        self._year_fraction_function = year_fraction_function

    def year_fraction(self, start_date: date, end_date: date) -> float:
        """
        Calculates the year fraction between two dates.
        :param start_date: Start date.
        :param end_date: End date.
        :return: Year fraction as a float.
        """
        return self._year_fraction_function(start_date, end_date)

    @staticmethod
    def of(convention: str) -> "DayCount":
        """
        Factory method to get a DayCount instance based on a convention name.
        :param convention: The day count convention name (e.g., "A360", "A365", "ACT/ACT").
        :return: Corresponding DayCount instance.
        :raises ValueError: If the convention is unknown.
        """
        convention = convention.upper()

        if convention == "A360":
            return DayCount(DayCount._actual_360)
        elif convention == "A365":
            return DayCount(DayCount._actual_365)
        elif convention == "ACT/ACT":
            return DayCount(DayCount._actual_actual)
        else:
            raise ValueError(f"Unknown day count convention: {convention}")

    @staticmethod
    def _actual_360(start_date: date, end_date: date) -> float:
        """
        Actual/360 convention: Calculates year fraction based on 360 days in a year.
        """
        delta = (end_date - start_date).days
        return delta / 360.0

    @staticmethod
    def _actual_365(start_date: date, end_date: date) -> float:
        """
        Actual/365 convention: Calculates year fraction based on 365 days in a year.
        """
        delta = (end_date - start_date).days
        return delta / 365.0

    @staticmethod
    def _actual_actual(start_date: date, end_date: date) -> float:
        """
        Actual/Actual convention: Calculates year fraction based on actual days in a year.
        """
        delta = (end_date - start_date).days
        year_length = 366 if start_date.year % 4 == 0 else 365
        return delta / year_length
