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

class InterpolationMethod:
    """
    Represents various interpolation methods with associated codes.
    """
    LINEAR_DF = "LDF"
    LINEAR_ZERO = "LZ"
    FLAT_FORWARD = "FF"
    CUBIC_SPLINE = "CS"
    MONOTONE_CONVEX = "MC"

    _codes = {
        LINEAR_DF: "LDF",
        LINEAR_ZERO: "LZ",
        FLAT_FORWARD: "FF",
        CUBIC_SPLINE: "CS",
        MONOTONE_CONVEX: "MC",
    }

    @classmethod
    def from_code(cls, code):
        """
        Get the interpolation method corresponding to the given code.
        :param code: Code string for the interpolation method.
        :return: Interpolation method as a string. Defaults to LINEAR_ZERO.
        """
        for method, method_code in cls._codes.items():
            if method_code == code:
                return method
        return cls.LINEAR_ZERO  # Default
