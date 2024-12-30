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
from datetime import date
from abc import ABC, abstractmethod

from yield_curve.engine.date.abs_holiday_calendar import HolidayCalendar
from yield_curve.engine.date.business_day_convention import BusinessDayConvention


class StandardBusinessDayConventions(BusinessDayConvention):
    """
    Standard business day conventions as an enum.
    Each convention implements the BusinessDayConvention interface.
    """

    NO_ADJUST = "NoAdjust"
    FOLLOWING = "Following"
    MODIFIED_FOLLOWING = "ModifiedFollowing"
    MODIFIED_FOLLOWING_BI_MONTHLY = "ModifiedFollowingBiMonthly"
    PRECEDING = "Preceding"
    MODIFIED_PRECEDING = "ModifiedPreceding"
    NEAREST = "Nearest"

    @staticmethod
    def from_name(name: str) -> "StandardBusinessDayConventions":
        """
        Get the enum instance corresponding to the given name.
        :param name: The string representation of the convention.
        :return: The matching enum instance.
        :raises ValueError: If no matching convention is found.
        """
        for convention in StandardBusinessDayConventions:
            if convention.value == name:
                return convention
        raise ValueError(f"Unknown business day convention: {name}")

    def __init__(self, value: str):
        """
        Allows the class to construct an enum instance directly from its name.
        """
        if isinstance(value, str):
            try:
                # Validate and map the input string
                validated_instance = StandardBusinessDayConventions.from_name(value)
                self._value_ = validated_instance.value
            except ValueError as e:
                raise ValueError(f"Error constructing StandardBusinessDayConventions: {e}")

    def adjust(self, input_date: date, calendar: HolidayCalendar) -> date:
        if self == StandardBusinessDayConventions.NO_ADJUST:
            return input_date

        if self == StandardBusinessDayConventions.FOLLOWING:
            return calendar.next_or_same(input_date)

        if self == StandardBusinessDayConventions.MODIFIED_FOLLOWING:
            adjusted = calendar.next_or_same(input_date)
            if adjusted.month != input_date.month:
                return calendar.previous_business_day(input_date)
            return adjusted

        if self == StandardBusinessDayConventions.MODIFIED_FOLLOWING_BI_MONTHLY:
            adjusted = calendar.next_or_same(input_date)
            if adjusted.month != input_date.month or (adjusted.day > 15 and input_date.day <= 15):
                return calendar.previous_business_day(input_date)
            return adjusted

        if self == StandardBusinessDayConventions.PRECEDING:
            return calendar.previous_or_same(input_date)

        if self == StandardBusinessDayConventions.MODIFIED_PRECEDING:
            adjusted = calendar.previous_or_same(input_date)
            if adjusted.month != input_date.month:
                return calendar.next_business_day(input_date)
            return adjusted

        if self == StandardBusinessDayConventions.NEAREST:
            if calendar.is_business_day(input_date):
                return input_date
            if input_date.weekday() in (6, 0):  # Sunday or Monday
                return calendar.next_business_day(input_date)
            else:
                return calendar.previous_business_day(input_date)

    def get_name(self) -> str:
        """
        Returns the name of the business day convention.
        """
        return self.value
