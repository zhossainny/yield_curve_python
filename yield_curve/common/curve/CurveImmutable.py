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

from yield_curve.common.curve.Exception.CurveExtrapolationException import CurveExtrapolationException
from yield_curve.common.curve import Curve, CurveInterpolator
from yield_curve.common.curve.InterpolationMethod import InterpolationMethod
from yield_curve.common.curve import FlatForwardInterpolator
from yield_curve.common.curve.LinearDiscountFactorInterpolator import LinearDiscountFactorInterpolator
from yield_curve.common.curve.LinearZeroInterpolator import LinearZeroInterpolator
from yield_curve.common.curve.CubicInterpolator import CubicInterpolator
from yield_curve.common.curve.MonotoneConvexInterpolator import MonotoneConvexInterpolator
from yield_curve.common.curve.FlatForwardInterpolator import FlatForwardInterpolator
import numpy as np  # For copying arrays

from yield_curve.common.util.functions import binary_search


class CurveImmutable(Curve):
    """
    Immutable implementation of the Curve interface.
    """

    def __init__(self, curve: Curve):
        """
        Initialize CurveImmutable with a Curve instance.
        Validates and copies the data to make it immutable.
        """
        if curve is None:
            raise ValueError("null curve")

        x = curve.get_x()
        y = curve.get_y()

        if x is None:
            raise ValueError("null x")
        if y is None:
            raise ValueError("null y")
        if len(x) != len(y):
            raise ValueError("x.length != y.length")

        interpolation_method = curve.get_interpolation_method()
        if interpolation_method is None:
            raise ValueError("null interpolation method")

        # Copy the data to ensure immutability
        self.x = np.copy(x)
        self.y = np.copy(y)
        self.interpolation_method = interpolation_method

        # Build the interpolator
        self.interpolator = self.build_interpolator(self.interpolation_method)

    def get_x(self):
        """Return a copy of x values."""
        return np.copy(self.x)

    def get_y(self):
        """Return a copy of y values."""
        return np.copy(self.y)

    def get_interpolation_method(self):
        """Return the interpolation method."""
        return self.interpolation_method

    def interpolate(self, ax: float) -> float:
        """
        Interpolate a single value.
        :param ax: Value to interpolate.
        :return: Interpolated value.
        """
        index = binary_search(self.x, ax)
        if index >= 0:
            return self.y[index]

        index = -index - 2
        if index == -1:
            raise CurveExtrapolationException("Extrapolation beyond short end")
        if index == len(self.x) - 1:
            raise CurveExtrapolationException("Extrapolation beyond long end")

        return self.interpolator.interpolate(index, ax)

    def interpolate_array(self, ax: list, result: list = None):
        """
        Interpolate an array of values.
        :param ax: Array of values to interpolate.
        :param result: Optional list to store the results.
        :return: Result list with interpolated values.
        """
        if result is None:
            result = [0] * len(ax)

        for i, val in enumerate(ax):
            if val < self.x[0]:
                raise CurveExtrapolationException("Extrapolation beyond short end")
            if val > self.x[-1]:
                raise CurveExtrapolationException("Extrapolation beyond long end")

            result[i] = self.interpolate(val)

        return result

    def build_interpolator(self, interpolation_method: InterpolationMethod) -> CurveInterpolator:
        """
        Build an interpolator based on the interpolation method.
        """
        self.interpolator: CurveInterpolator
        if interpolation_method == InterpolationMethod.LINEAR_DF:
            interpolator = LinearDiscountFactorInterpolator(self)
        elif interpolation_method == InterpolationMethod.LINEAR_ZERO:
            interpolator = LinearZeroInterpolator(self)
        elif interpolation_method == InterpolationMethod.FLAT_FORWARD:
            interpolator = FlatForwardInterpolator(self)
        elif interpolation_method == InterpolationMethod.CUBIC_SPLINE:
            interpolator = CubicInterpolator(self)
        elif interpolation_method == InterpolationMethod.MONOTONE_CONVEX:
            interpolator = MonotoneConvexInterpolator(self)
        else:
            raise ValueError("Unsupported interpolation method")

        interpolator.initialize()
        return interpolator

    def __eq__(self, other):
        """Equality check for CurveImmutable."""
        if self is other:
            return True
        if not isinstance(other, CurveImmutable):
            return False

        return (
                np.array_equal(self.x, other.x) and
                np.array_equal(self.y, other.y) and
                self.interpolation_method == other.interpolation_method
        )

    def __hash__(self):
        """Generate a hash for CurveImmutable."""
        return hash((tuple(self.x), tuple(self.y), self.interpolation_method))

    def __str__(self):
        """String representation of CurveImmutable."""
        return (
            f"{self.__class__.__name__}("
            f"x={self.x}, y={self.y}, "
            f"interpolation_method={self.interpolation_method})"
        )
