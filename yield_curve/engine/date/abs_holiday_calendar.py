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
from datetime import date, timedelta
from typing import Generator, Callable

from yield_curve.engine.date.named import Named


class HolidayCalendar(Named, ABC):
    """
    A holiday calendar, classifying dates as holidays or business days.
    """

    @abstractmethod
    def is_holiday(self, date: date) -> bool:
        """
        Checks if the specified date is a holiday.
        A weekend is treated as a holiday.
        :param date: The date to check
        :return: True if the specified date is a holiday
        """
        pass

    def is_business_day(self, date: date) -> bool:
        """
        Checks if the specified date is a business day.
        This is the opposite of is_holiday.
        :param date: The date to check
        :return: True if the specified date is a business day
        """
        return not self.is_holiday(date)

    def adjust_by(self, amount: int) -> Callable[[date], date]:
        """
        Returns an adjuster that changes the date by a number of business days.
        :param amount: The number of business days to adjust by
        :return: A callable that adjusts a date by the specified amount
        """
        return lambda d: self.shift(d, amount)

    def shift(self, date: date, amount: int) -> date:
        """
        Shifts the date by the specified number of business days.
        :param date: The date to adjust
        :param amount: The number of business days to adjust by
        :return: The shifted date
        """
        adjusted = date
        step = 1 if amount > 0 else -1
        for _ in range(abs(amount)):
            adjusted = self.next(adjusted) if step > 0 else self.previous(adjusted)
        return adjusted

    def next(self, date: date) -> date:
        """
        Finds the next business day, always returning a later date.
        :param date: The date to adjust
        :return: The first business day after the input date
        """
        next_date = date + timedelta(days=1)
        return self.next(next_date) if self.is_holiday(next_date) else next_date

    def next_or_same(self, date: date) -> date:
        """
        Finds the next business day, returning the input date if it is a business day.
        :param date: The date to adjust
        :return: The input date if it is a business day, or the next business day
        """
        return date if not self.is_holiday(date) else self.next(date)

    def previous(self, date: date) -> date:
        """
        Finds the previous business day, always returning an earlier date.
        :param date: The date to adjust
        :return: The first business day before the input date
        """
        prev_date = date - timedelta(days=1)
        return self.previous(prev_date) if self.is_holiday(prev_date) else prev_date

    def previous_or_same(self, date: date) -> date:
        """
        Finds the previous business day, returning the input date if it is a business day.
        :param date: The date to adjust
        :return: The input date if it is a business day, or the previous business day
        """
        return date if not self.is_holiday(date) else self.previous(date)

    @abstractmethod
    def get_id(self):
        """
        Gets the identifier for the calendar.
        :return: The identifier
        """
        pass

    def get_name(self) -> str:
        """
        Gets the name that identifies this calendar.
        :return: The name
        """
        return self.get_id().get_name()
