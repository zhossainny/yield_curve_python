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


