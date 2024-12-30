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
