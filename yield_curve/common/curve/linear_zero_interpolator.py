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

from yield_curve.common.curve.curve_interpolator import CurveInterpolator, CurveException


class LinearZeroInterpolator(CurveInterpolator):
    def __init__(self, curve):
        """
        Initialize the LinearZeroInterpolator with a Curve instance.
        :param curve: Instance of a class implementing the Curve interface.
        """
        self.curve = curve
        self.x = None
        self.y = None

    def initialize(self):
        """
        Prepare any transformations or setup required for interpolation.
        This method initializes x and y arrays based on the given curve.
        """
        self.x = self.curve.get_x()
        self.y = self.curve.get_y()

    def interpolate(self, low_index: int, ax: float) -> float:
        """
        Interpolate a value using the linear zero method.
        :param low_index: The lower index for interpolation.
        :param ax: The value to interpolate.
        :return: Interpolated value as a float.
        :raises CurveException: If the value is not bracketed.
        """
        x1 = self.x[low_index]
        x2 = self.x[low_index + 1]
        y1 = self.y[low_index]
        y2 = self.y[low_index + 1]

        if not (x1 <= ax <= x2):
            raise CurveException("Not bracketed")

        ay = y1 + (ax - x1) * (y2 - y1) / (x2 - x1)
        return ay
