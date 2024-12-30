from yield_curve.common.curve.Exception.CurveException import CurveException
from yield_curve.common.curve.Exception.CurveExtrapolationException import CurveExtrapolationException
from yield_curve.common.curve import Curve, CurveInterpolator
from yield_curve.common.curve.Curve import Curve
from yield_curve.common.curve.InterpolationMethod import InterpolationMethod
from yield_curve.common.curve import FlatForwardInterpolator
from yield_curve.common.curve.LinearDiscountFactorInterpolator import LinearDiscountFactorInterpolator
from yield_curve.common.curve.LinearZeroInterpolator import LinearZeroInterpolator
from yield_curve.common.curve.CubicInterpolator import CubicInterpolator
from yield_curve.common.curve.MonotoneConvexInterpolator import MonotoneConvexInterpolator
from yield_curve.common.curve.FlatForwardInterpolator import FlatForwardInterpolator
import numpy as np  # For copying arrays

from yield_curve.common.util.functions import binary_search


class CurveImpl(Curve):
    """
    Implementation of the Curve interface.
    """

    def __init__(self, x: np.ndarray, y: np.ndarray, interp_method: InterpolationMethod):
        """
        Initialize the CurveImpl with x and y values and an interpolation method.
        Validates the inputs and builds the interpolator.
        """
        if x is None:
            raise ValueError("x cannot be None")
        if y is None:
            raise ValueError("y cannot be None")
        if interp_method is None:
            raise ValueError("interp_method cannot be None")
        if len(x) != len(y):
            raise CurveException(f"x and y vectors must have the same length: {len(x)} != {len(y)}")
        if not np.all(np.diff(x) > 0):
            raise CurveException("x values must be in ascending order and not duplicated")

        self.x = x
        self.y = y
        self.interp_method = interp_method
        self.interpolator = self.build_interpolator()

    def interpolate_array2(self, ax):
        result = np.zeros_like(len(ax))
        self.interpolate_array(ax, result)
        return result

    def get_x(self) -> np.ndarray:
        """Return the x values."""
        return self.x

    def get_y(self) -> np.ndarray:
        """Return the y values."""
        return self.y

    def get_interpolation_method(self) -> InterpolationMethod:
        """Return the interpolation method."""
        return self.interp_method

    def interpolate(self, ax: float) -> float:
        """
        Interpolate a single value.
        :param ax: The value to interpolate.
        :return: The interpolated value.
        """
        index = binary_search(self.x, ax)
        if index >= 0:
            return self.y[index]

        index = -index - 2
        if index == -1:
            raise CurveExtrapolationException(f"Extrapolation beyond the short end of the curve: {ax}")
        if index == len(self.x) - 1:
            raise CurveExtrapolationException(f"Extrapolation beyond the long end of the curve: {ax}")

        return self.interpolator.interpolate(index, ax)

    def interpolate_array(self, ax: np.ndarray, result: np.ndarray = None) -> np.ndarray:
        """
        Interpolate an array of values.
        :param ax: Array of values to interpolate.
        :param result: Optional array to store the results.
        :return: The interpolated results.
        """
        if result is None:
            result = np.zeros_like(ax)

        for i, val in enumerate(ax):
            if val < self.x[0]:
                raise CurveExtrapolationException(f"Extrapolation beyond the short end of the curve: {val}")
            if val > self.x[-1]:
                raise CurveExtrapolationException(f"Extrapolation beyond the long end of the curve: {val}")

            result[i] = self.interpolate(val)

        return result

    def build_interpolator(self):
        """
        Build the interpolator based on the interpolation method.
        :return: An instance of the appropriate interpolator.
        """
        if self.interp_method == InterpolationMethod.LINEAR_DF:
            interpolator = LinearDiscountFactorInterpolator(self)
        elif self.interp_method == InterpolationMethod.LINEAR_ZERO:
            interpolator = LinearZeroInterpolator(self)
        elif self.interp_method == InterpolationMethod.FLAT_FORWARD:
            interpolator = FlatForwardInterpolator(self)
        elif self.interp_method == InterpolationMethod.CUBIC_SPLINE:
            interpolator = CubicInterpolator(self)
        elif self.interp_method == InterpolationMethod.MONOTONE_CONVEX:
            interpolator = MonotoneConvexInterpolator(self)
        else:
            raise CurveException(f"Unsupported interpolation method: {self.interp_method}")

        interpolator.initialize()
        return interpolator

    def update(self):
        """
        Reinitialize the interpolator after modifying x or y values.
        """
        self.interpolator.initialize()

    def copy(self):
        """
        Create a copy of the CurveImpl instance.
        :return: A new CurveImpl instance with the same data.
        """
        new_x = np.copy(self.x)
        new_y = np.copy(self.y)
        return CurveImpl(new_x, new_y, self.interp_method)

    def __eq__(self, other):
        """Equality check for CurveImpl."""
        if not isinstance(other, CurveImpl):
            return False

        return (
                np.array_equal(self.x, other.x)
                and np.array_equal(self.y, other.y)
                and self.interp_method == other.interp_method
        )

    def __hash__(self):
        """Generate a hash for CurveImpl."""
        return hash((tuple(self.x), tuple(self.y), self.interp_method))

    def __str__(self):
        """String representation of CurveImpl."""
        return (
            f"CurveImpl("
            f"x=[{self.x[0]}, ..., {self.x[-1]}], "
            f"y=[{self.y[0]}, ..., {self.y[-1]}], "
            f"interp_method={self.interp_method})"
        )
