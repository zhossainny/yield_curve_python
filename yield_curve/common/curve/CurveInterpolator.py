from abc import ABC, abstractmethod


class CurveException(Exception):
    """Custom exception for curve-related errors."""
    pass


class CurveInterpolator(ABC):
    """Abstract Base Class for Curve Interpolators."""

    @abstractmethod
    def interpolate(self, low_index: int, x: float) -> float:
        """
        Interpolate a value.
        :param low_index: The lower index for interpolation.
        :param x: The value to interpolate.
        :return: Interpolated value as a float.
        :raises CurveException: If an error occurs during interpolation.
        """
        pass

    @abstractmethod
    def initialize(self):
        """
        Prepare any transformations or setup required for interpolation.
        """
        pass
