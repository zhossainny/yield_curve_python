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

from yield_curve.engine.curve_adjustment.curve_adjuster import CurveAdjuster


class PricingFunction(ABC):
    @abstractmethod
    def value(self, adjuster: CurveAdjuster) -> float:
        """
        Calculate the value based on the given CurveAdjuster.

        :param adjuster: CurveAdjuster instance used for calculation.
        :return: Calculated value as a float.
        :raises EngineException: If an error occurs during the calculation.
        """
        pass

    @abstractmethod
    def curve_date(self) -> float:
        """
        Get the curve date.

        :return: Curve date as a float.
        """
        pass
