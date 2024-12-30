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
from typing import List, Set


class ImmutableHolidayCalendar:
    """
    Simplified ImmutableHolidayCalendar implementation to match test requirements.
    """

    def __init__(self, calendar_id: str, holidays: List[date], weekend_days: Set[int]):
        """
        Initialize the holiday calendar with a unique ID, holiday dates, and weekend days.
        :param calendar_id: The unique identifier for the calendar.
        :param holidays: A list of holiday dates.
        :param weekend_days: A set of integers representing weekend days (e.g., {5, 6} for Saturday and Sunday).
        """
        self._id = calendar_id
        self._holidays = holidays
        self._weekend_days = weekend_days

    def is_holiday(self, input_date: date) -> bool:
        """
        Checks if the specified date is a holiday or a weekend.
        :param input_date: The date to check.
        :return: True if the date is a holiday or weekend, False otherwise.
        """
        return input_date.weekday() in self._weekend_days or input_date in self._holidays

    def get_id(self) -> str:
        """
        Gets the unique identifier for this holiday calendar.
        :return: The identifier string.
        """
        return self._id

    def to_dict(self) -> dict:
        """
        Converts the holiday calendar to a dictionary format expected by tests.
        :return: A dictionary with `id`, `holidays`, and `weekends`.
        """
        return {
            "id": self._id,
            "holidays": self._holidays,
            "weekends": self._weekend_days,
        }
