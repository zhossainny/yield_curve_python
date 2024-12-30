from abc import ABC, abstractmethod
from math import exp

from yield_curve.common.util.date_convert import DateConvert


class CurveException(Exception):
    """Custom exception for curve-related errors."""
    pass


class Curve(ABC):
    """Abstract Base Class representing a curve."""

    @abstractmethod
    def get_x(self):
        """Get the X values (must be in ascending order)."""
        pass

    @abstractmethod
    def get_y(self):
        """Get the Y values."""
        pass

    @abstractmethod
    def get_interpolation_method(self):
        """Get the interpolation method."""
        pass

    @abstractmethod
    def interpolate(self, x):
        """
        Interpolate a single value.
        :param x: Value to interpolate.
        :raises CurveException: If an error occurs during interpolation.
        """
        # return double
        pass

    @abstractmethod
    def interpolate_array(self, x, result=None):
        """
        Interpolate an array of values.
        :param x: Array of values to interpolate.
        :param result: Optional array to store results.
        :raises CurveException: If an error occurs during interpolation.
        """
        # retur void
        pass

    @abstractmethod
    def interpolate_array2(self, x):
        """
        Interpolate an array of values.
        :param x: Array of values to interpolate.
        :param result: Optional array to store results.
        :raises CurveException: If an error occurs during interpolation.
        """
        # return array of double
        pass

    def interpolate_local_date(self, local_date):
        """
        Interpolate a value based on a LocalDate.
        :param local_date: The date to interpolate.
        :param date_convert: A callable to convert LocalDate to double.
        :return: Interpolated value.
        """
        try:
            return self.interpolate(DateConvert.local_date_to_double(local_date))
        except Exception as exception:
            raise ValueError("Invalid interpolation: " + str(exception))

    def year_fraction(self, local_date):
        """
        Calculate the year fraction for a given LocalDate.
        :param local_date: The date to calculate the year fraction for.
        :param date_convert: A callable to convert LocalDate to double.
        :return: Year fraction.
        :raises ValueError: If the year fraction is invalid.
        """
        year_fraction = DateConvert.local_date_to_double(local_date - self.get_x()[0])/365
        if year_fraction < 0:
            raise ValueError(f"Invalid yearFraction={year_fraction}")
        return year_fraction

    def discount_factor(self, local_date, date_convert):
        """
        Calculate the discount factor for a given LocalDate.
        :param local_date: The date for the discount factor calculation.
        :param date_convert: A callable to convert LocalDate to double.
        :return: Discount factor.
        """
        return exp(
            -1.0 * self.interpolate_local_date(local_date) * self.year_fraction(local_date))
