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
from datetime import date

from yield_curve.engine.date.abs_holiday_calendar import HolidayCalendar


class ExtendedEnum:
    """
    Placeholder for ExtendedEnum functionality.
    Provides access to predefined instances or helps register new instances.
    """
    _registry = {}

    @classmethod
    def register(cls, name: str, instance):
        cls._registry[name] = instance

    @classmethod
    def get(cls, name: str):
        return cls._registry.get(name)

    @classmethod
    def available_names(cls):
        return list(cls._registry.keys())


class BusinessDayConvention(ABC):
    """
    Abstract base class representing a business day convention.
    Determines how to adjust a date if it falls on a non-business day.
    """

    @staticmethod
    def of(unique_name: str):
        """
        Obtains an instance of the business day convention from its unique name.
        :param unique_name: The unique name of the convention.
        :return: The BusinessDayConvention instance.
        :raises ValueError: If the name is not found.
        """
        instance = ExtendedEnum.get(unique_name)
        if instance is None:
            raise ValueError(f"BusinessDayConvention '{unique_name}' not found.")
        return instance

    @staticmethod
    def extended_enum():
        """
        Gets the extended enum helper for accessing all registered instances.
        :return: The ExtendedEnum helper.
        """
        return ExtendedEnum

    @abstractmethod
    def adjust(self, input_date: date, calendar: HolidayCalendar) -> date:
        """
        Adjusts the date if it is not a business day.
        :param input_date: The date to adjust.
        :param calendar: The holiday calendar to use for determining business days.
        :return: The adjusted date.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Gets the name of the business day convention.
        :return: The name of the convention.
        """
        pass


