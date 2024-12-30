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

from math import exp, log, pow

from yield_curve.common.curve.curve_interpolator import CurveInterpolator


class MonotoneConvexInterpolator(CurveInterpolator):
    ONETHIRD = 1.0 / 3.0
    TWOTHIRDS = 2.0 / 3.0

    def __init__(self, curve):
        """
        Initialize the MonotoneConvexInterpolator with a Curve instance.
        :param curve: Instance of a class implementing the Curve interface.
        """
        self.curve = curve
        self.terms = None
        self.values = None
        self.f = None
        self.fdiscrete = None

    def initialize(self):
        """
        Prepare any transformations or setup required for interpolation.
        This method initializes the terms, values, f, and fdiscrete arrays based on the given curve.
        """
        n = len(self.curve.get_x()) - 1
        self.values = self.curve.get_y()
        self.terms = [0.0] * (n + 1)
        self.f = [0.0] * (n + 1)
        self.fdiscrete = [0.0] * (n + 1)

        # Convert x values to years
        for i in range(1, n + 1):
            self.terms[i] = (self.curve.get_x()[i] - self.curve.get_x()[0]) / 365.0

        # Calculate discrete forward rates
        for i in range(1, n + 1):
            self.fdiscrete[i] = (self.terms[i] * self.values[i] - self.terms[i - 1] * self.values[i - 1]) / (
                    self.terms[i] - self.terms[i - 1])

        # Calculate continuous forward rates
        for i in range(1, n):
            self.f[i] = (self.terms[i] - self.terms[i - 1]) / (
                    self.terms[i + 1] - self.terms[i - 1]) * self.fdiscrete[i + 1] + (
                                self.terms[i + 1] - self.terms[i]) / (
                                self.terms[i + 1] - self.terms[i - 1]) * self.fdiscrete[i]

        # Boundary conditions for f[0] and f[n]
        self.f[0] = self.collar(0.0, self.fdiscrete[1] - 0.5 * (self.f[1] - self.fdiscrete[1]),
                                2.0 * self.fdiscrete[1])
        self.f[n] = self.collar(0.0, self.fdiscrete[n] - 0.5 * (self.f[n - 1] - self.fdiscrete[n]),
                                2.0 * self.fdiscrete[n])

        # Final adjustments for f[i]
        for i in range(1, n):
            self.f[i] = self.collar(0.0, self.f[i], 2.0 * min(self.fdiscrete[i], self.fdiscrete[i + 1]))

    def interpolate(self, low_index: int, ax: float) -> float:
        """
        Interpolate a value using the monotone convex method.
        :param low_index: The lower index for interpolation.
        :param ax: The value to interpolate.
        :return: Interpolated value as a float.
        :raises CurveException: If the value is not bracketed.
        """
        i = low_index
        L = self.terms[i + 1] - self.terms[i]
        term = (ax - self.curve.get_x()[0]) / 365.0
        x = (term - self.terms[i]) / L
        g0 = self.f[i] - self.fdiscrete[i + 1]
        g1 = self.f[i + 1] - self.fdiscrete[i + 1]
        G = 0.0

        if term <= 0.0:
            return self.f[0]

        if x == 0.0 or x == 1.0:
            G = 0.0
        elif (g0 <= 0.0 and -0.5 * g0 <= g1 <= -2.0 * g0) or (g0 > 0.0 and -0.5 * g0 >= g1 >= -2.0 * g0):
            # Zone 1
            G = L * (g0 * self.cubic_eval(x, 1.0, -2.0, 1.0) + g1 * self.cubic_eval(x, 0.0, 0.0, 0.0))
        elif (g0 <= 0.0 and -2.0 * g0 < g1 <= -0.5 * g0) or (g0 > 0.0 and -2.0 * g0 > g1 >= -0.5 * g0):
            # Zone 2
            eta = g1 / (g1 - g0)
            if x <= eta:
                G = g0 * (term - self.terms[i])
            else:
                G = g0 * (term - self.terms[i]) + (g1 - g0) * self.cube(x - eta) / self.square(eta - x)
        elif g0 == 0.0 and g1 == 0.0:
            # Zone 3
            G = 0.0
        else:
            # Zone 4
            eta = g1 / (g1 + g0)
            A = -g0 * g1 / (g0 + g1)
            if x <= eta:
                G = L * (g0 * self.cubic_eval(x, 1.0, -2.0, 1.0) + g1 * self.cubic_eval(x, 0.0, 0.0, 0.0))
            else:
                G = L * (g0 * self.cubic_eval(x, 1.0, -1.0, 1.0) + g1 * self.cubic_eval(x, 0.0, 0.0, 0.0))

        return 1.0 / term * (G + self.terms[i] * self.values[i] + term * (self.fdiscrete[i + 1] - self.f[i]))

    @staticmethod
    def collar(a, b, c):
        """Return max(a, min(b, c))."""
        return max(a, min(b, c))

    @staticmethod
    def cubic_eval(x, a, b, c):
        """Evaluate ax^3 + bx^2 + cx."""
        return a * pow(x, 3) + b * pow(x, 2) + c * x

    @staticmethod
    def cube(x):
        """Return x^3."""
        return pow(x, 3)

    @staticmethod
    def square(x):
        """Return x^2."""
        return pow(x, 2)
